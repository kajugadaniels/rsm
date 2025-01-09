from base.forms import *
from account.models import *
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test

def is_superuser(user):
    return user.is_superuser

def dashboard(request):
    return render(request, 'pages/dashboard.html')