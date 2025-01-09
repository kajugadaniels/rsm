from base.forms import *
from account.models import *
from django.urls import reverse
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
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
    roles = Role.objects.all().order_by('-id')
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
            messages.success(
                request, 
                _("The role '%(role)s' has been created successfully.") % {'role': role.name}
            )
            return redirect(reverse('base:getRoles'))
        else:
            messages.error(request, _("Please correct the errors below and try again."))
    else:
        form = RoleForm()
    
    context = {
        'form': form,
        'title': _('Add New Role'),
    }
    return render(request, 'pages/roles/create.html', context)

@login_required
@permission_required('account.change_role', raise_exception=True)
def editRole(request, slug):
    """
    Edit an existing Role instance identified by its slug.
    """
    role = get_object_or_404(Role, slug=slug)
    
    if request.method == 'POST':
        form = RoleForm(request.POST, instance=role)
        if form.is_valid():
            role = form.save()
            messages.success(
                request, 
                _("The role '%(role)s' has been updated successfully.") % {'role': role.name}
            )
            return redirect(reverse('base:getRoles'))
        else:
            messages.error(request, _("Please correct the errors below and try again."))
    else:
        form = RoleForm(instance=role)
    
    context = {
        'form': form,
        'title': _('Edit Role: %(role)s') % {'role': role.name},
    }

    return render(request, 'pages/roles/edit.html', context)

@login_required
@permission_required('account.delete_role', raise_exception=True)
def deleteRole(request, slug):
    """
    Delete an existing Role instance identified by its slug.
    """
    role = get_object_or_404(Role, slug=slug)
    
    if request.method == 'POST':
        role.delete()
        messages.success(
            request, 
            _("The role '%(role)s' has been deleted successfully.") % {'role': role.name}
        )
        return redirect(reverse('base:getRoles'))
    
    context = {
        'role': role,
    }

    return render(request, 'pages/roles/delete.html', context)

@ login_required
@ permission_required('base.view_product', raise_exception=True)
def getProducts(request):
    """
    Retrieve and display all Product instances.
    """
    products = Product.objects.all().order_by('-created_at')
    context = {
        'products': products,
    }
    return render(request, 'pages/products/index.html', context)

@ login_required
@ permission_required('base.add_product', raise_exception=True)
def addProduct(request):
    """
    Create a new Product instance.
    """
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            messages.success(
                request, 
                _("The product '%(product)s' has been created successfully.") % {'product': product.name}
            )
            return redirect(reverse('base:getProducts'))
        else:
            messages.error(request, _("Please correct the errors below and try again."))
    else:
        form = ProductForm()
    
    context = {
        'form': form,
        'title': _('Add New Product'),
    }
    return render(request, 'pages/products/create.html', context)