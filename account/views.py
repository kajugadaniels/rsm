from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout, update_session_auth_hash

def userLogin(request):
    context = {
        # 
    }

    return render(request, 'pages/auth/login.html', context)