from account.forms import *
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate, login as auth_login, logout

def userLogin(request):
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, _("You have been logged out as you were already logged in with another account."))

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data.get('user')
            auth_login(request, user)
            messages.success(request, _("You have successfully logged in."))
            return redirect(reverse('base:dashboard'))
        else:
            # Extract form errors and display them as individual messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
            messages.error(request, _("Please address the errors below and try again."))
    else:
        form = LoginForm()

    context = {
        'form': form,
    }

    return render(request, 'pages/auth/login.html', context)

def userLogout(request):
    logout(request)
    return redirect('auth:login')

@login_required
def userProfile(request):
    user = request.user

    if request.method == 'POST':
        if 'profile_form' in request.POST:
            profile_form = UserProfileForm(request.POST, request.FILES, instance=user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Profil mis à jour avec succès.')
                return redirect('auth:userProfile')
            else:
                password_form = PasswordChangeForm(user=user)
        elif 'password_form' in request.POST:
            password_form = PasswordChangeForm(user=user, data=request.POST)
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, password_form.user)
                messages.success(request, 'Mot de passe modifié avec succès. Veuillez vous reconnecter.')
                logout(request)
                return redirect('auth:login')
            else:
                profile_form = UserProfileForm(instance=user)
    else:
        profile_form = UserProfileForm(instance=user)
        password_form = PasswordChangeForm(user=user)

    context = {
        'profile_form': profile_form,
        'password_form': password_form
    }

    return render(request, 'pages/auth/profile.html', context)