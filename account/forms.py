from django import forms
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User as AuthUser

class LoginForm(forms.Form):
    email = forms.EmailField(
        max_length=255,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email',
            'required': 'required',
            'id': 'emailaddress',
        }),
        label=_('Email address')
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password',
            'required': 'required',
            'id': 'password',
        }),
        label=_('Password')
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not AuthUser.objects.filter(email=email).exists():
            raise forms.ValidationError(_('No account found with this email address. Please check and try again.'))
        return email

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError(_('Incorrect password. Please try again.'))
            if not user.is_active:
                raise forms.ValidationError(_('Your account is inactive. Please contact support for assistance.'))
            cleaned_data['user'] = user
        return cleaned_data
