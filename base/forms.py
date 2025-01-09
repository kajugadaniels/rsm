from django import forms
from account.models import *
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Permission

class RoleForm(forms.ModelForm):
    """
    Form for creating and updating Role instances.
    """
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control',
        }),
        required=False,
        label=_('Permissions'),
        help_text=_('Select the permissions to assign to this role.'),
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
            raise forms.ValidationError(_('This role name is already in use. Please choose a different name.'))
        return name
