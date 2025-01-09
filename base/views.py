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

@login_required
@permission_required('account.add_role', raise_exception=True)
def addRole(request):
    """
    Create a new Role instance.
    """
    if request.method == 'POST':
        form = RoleForm(request.POST)
        if form.is_valid():
            role = form.save()
            form.save_m2m()  # Save the many-to-many data for permissions
            messages.success(request, _("The role '%(role)s' has been created successfully.") % {'role': role.name})
            return redirect(reverse('auth:getRoles'))
        else:
            messages.error(request, _("Please correct the errors below and try again."))
    else:
        form = RoleForm()
    
    context = {
        'form': form,
        'title': _('Add New Role'),
    }
    return render(request, 'pages/roles/create.html', context)