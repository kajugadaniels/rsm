from django import forms
from account.models import *
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
            raise forms.ValidationError(_('A role with this name already exists. Please choose a different name.'))
        return name
