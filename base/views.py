from base.forms import *
from account.models import *
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required, login_required

def dashboard(request):
    return render(request, 'pages/dashboard.html')

@login_required
@permission_required('account.view_role', raise_exception=True)
def getRoles(request):
    """
    Retrieve and display all Role instances.
    """
    roles = Role.objects.all().order_by('-created_at')
    context = {
        'roles': roles,
    }
    return render(request, 'pages/roles/index.html', context)