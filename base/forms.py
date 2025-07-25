from django import forms
from base.models import *
from account.models import *
from django.forms import formset_factory
from django.contrib.auth.models import Permission
from django.utils.translation import gettext_lazy as _

class RoleForm(forms.ModelForm):
    """
    Form for creating and updating Role instances.
    """
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input',
        }),
        required=False,
        label=_('Permissions'),
        help_text=_('Select the permissions that this role should have.')
    )

    class Meta:
        model = Role
        fields = ['name', 'permissions']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter role name',
                'required': 'required',
            }),
        }
        labels = {
            'name': _('Role Name'),
        }
        error_messages = {
            'name': {
                'required': _('Please enter a role name.'),
                'unique': _('This role name is already in use. Please choose a different name.'),
                'max_length': _('Role name cannot exceed 30 characters.'),
            },
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Role.objects.filter(name__iexact=name).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(
                _('A role with this name already exists. Please choose a different name.')
            )
        return name

class ProductForm(forms.ModelForm):
    """
    Form for creating and updating Product instances.
    """
    class Meta:
        model = Product
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product name',
                'required': 'required',
            }),
        }
        labels = {
            'name': _('Product Name'),
        }
        error_messages = {
            'name': {
                'required': _('Please enter a product name.'),
                'unique': _('This product name is already in use. Please choose a different name.'),
                'max_length': _('Product name cannot exceed 255 characters.'),
            },
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Product.objects.filter(name__iexact=name).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(_('A product with this name already exists. Please choose a different name.'))
        return name

class ClientForm(forms.ModelForm):
    """
    Form for creating and updating Client instances.
    """
    class Meta:
        model = Client
        fields = ['name', 'phone_number', 'destination']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter client name',
                'required': 'required',
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number',
                'required': 'required',
            }),
            'destination': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter destination',
                'required': 'required',
            }),
        }
        labels = {
            'name': _('Client Name'),
            'phone_number': _('Phone Number'),
            'destination': _('Destination'),
        }
        error_messages = {
            'name': {
                'required': _('Please enter the client name.'),
                'max_length': _('Client name cannot exceed 255 characters.'),
            },
            'phone_number': {
                'required': _('Please enter the phone number.'),
                'unique': _('This phone number is already in use. Please use a different one.'),
                'max_length': _('Phone number cannot exceed 15 characters.'),
            },
            'destination': {
                'required': _('Please enter the destination.'),
                'max_length': _('Destination cannot exceed 255 characters.'),
            },
        }

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if Client.objects.filter(phone_number=phone_number).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(_('This phone number is already in use. Please use a different one.'))
        return phone_number

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['client', 'destination']
        widgets = {
            'client': forms.Select(attrs={
                'class': 'form-control',
                'id': 'client-select',
                'required': 'required',
            }),
            'destination': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter destination',
            }),
        }
        labels = {
            'client': _('Client'),
            'destination': _('Destination'),
        }
        error_messages = {
            'client': {
                'required': _('Please select a client.'),
            },
            'destination': {
                'max_length': _('Destination cannot exceed 255 characters.'),
            },
        }

class OrderProductForm(forms.ModelForm):
    class Meta:
        model = OrderProduct
        fields = ['product', 'size', 'quantity', 'unit_price']
        widgets = {
            'product': forms.Select(attrs={
                'class': 'form-control product-select',
                'required': 'required',
            }),
            'size': forms.NumberInput(attrs={
                'class': 'form-control size-input',
                'min': '0',
                'step': '0.1',
                'required': 'required',
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control quantity-input',
                'min': '1',
                'required': 'required',
            }),
            'unit_price': forms.NumberInput(attrs={
                'class': 'form-control unit-price-input',
                'min': '0',
                'step': '0.01',
                'required': 'required',
            }),
        }
        labels = {
            'product': _('Product'),
            'size': _('Size'),
            'quantity': _('Quantity'),
            'unit_price': _('Unit Price'),
        }
        error_messages = {
            'product': {
                'required': _('Please select a product.'),
            },
            'size': {
                'required': _('Please enter the size.'),
                'invalid': _('Enter a valid size.'),
            },
            'quantity': {
                'required': _('Please enter the quantity.'),
                'invalid': _('Enter a valid quantity.'),
            },
            'unit_price': {
                'required': _('Please enter the unit price.'),
                'invalid': _('Enter a valid unit price.'),
            },
        }

    def clean_product(self):
        product = self.cleaned_data.get('product')
        if not Product.objects.filter(id=product.id).exists():
            raise forms.ValidationError(_('Selected product does not exist.'))
        return product

# Define the formset
OrderProductFormSet = formset_factory(OrderProductForm, extra=1, min_num=1, validate_min=True)