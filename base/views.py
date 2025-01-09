from base.forms import *
from base.models import *
from account.models import *
from django.urls import reverse
from django.db import transaction
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

@ login_required
@ permission_required('base.change_product', raise_exception=True)
def editProduct(request, slug):
    """
    Edit an existing Product instance identified by its slug.
    """
    product = get_object_or_404(Product, slug=slug)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save()
            messages.success(
                request, 
                _("The product '%(product)s' has been updated successfully.") % {'product': product.name}
            )
            return redirect(reverse('base:getProducts'))
        else:
            messages.error(request, _("Please correct the errors below and try again."))
    else:
        form = ProductForm(instance=product)
    
    context = {
        'form': form,
        'title': _('Edit Product: %(product)s') % {'product': product.name},
    }

    return render(request, 'pages/products/edit.html', context)

@ login_required
@ permission_required('base.delete_product', raise_exception=True)
def deleteProduct(request, slug):
    """
    Delete an existing Product instance identified by its slug.
    """
    product = get_object_or_404(Product, slug=slug)
    
    if request.method == 'POST':
        product.delete()
        messages.success(
            request, 
            _("The product '%(product)s' has been deleted successfully.") % {'product': product.name}
        )
        return redirect(reverse('base:getProducts'))
    
    context = {
        'product': product,
    }

    return render(request, 'pages/products/delete.html', context)

@login_required
@permission_required('base.view_client', raise_exception=True)
def getClients(request):
    """
    Retrieve and display all Client instances.
    """
    clients = Client.objects.all().order_by('-created_at')
    context = {
        'clients': clients,
    }
    return render(request, 'pages/clients/index.html', context)

@login_required
@permission_required('base.add_client', raise_exception=True)
def addClient(request):
    """
    Create a new Client instance.
    """
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save()
            messages.success(
                request, 
                _("The client '%(client)s' has been created successfully.") % {'client': client.name}
            )
            return redirect(reverse('base:getClients'))
        else:
            messages.error(request, _("Please correct the errors below and try again."))
    else:
        form = ClientForm()
    
    context = {
        'form': form,
        'title': _('Add New Client'),
    }
    return render(request, 'pages/clients/create.html', context)

@login_required
@permission_required('base.change_client', raise_exception=True)
def editClient(request, id):
    """
    Edit an existing Client instance identified by its ID.
    """
    client = get_object_or_404(Client, id=id)
    
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            client = form.save()
            messages.success(
                request, 
                _("The client '%(client)s' has been updated successfully.") % {'client': client.name}
            )
            return redirect(reverse('base:getClients'))
        else:
            messages.error(request, _("Please correct the errors below and try again."))
    else:
        form = ClientForm(instance=client)
    
    context = {
        'form': form,
        'title': _('Edit Client: %(client)s') % {'client': client.name},
    }

    return render(request, 'pages/clients/edit.html', context)

@login_required
@permission_required('base.delete_client', raise_exception=True)
def deleteClient(request, id):
    """
    Delete an existing Client instance identified by its ID.
    """
    client = get_object_or_404(Client, id=id)
    
    if request.method == 'POST':
        client.delete()
        messages.success(
            request, 
            _("The client '%(client)s' has been deleted successfully.") % {'client': client.name}
        )
        return redirect(reverse('base:getClients'))
    
    context = {
        'client': client,
    }

    return render(request, 'pages/clients/delete.html', context)

@login_required
@permission_required('base.view_order', raise_exception=True)
def getOrders(request):
    orders = Order.objects.all().order_by('-created_at')
    context = {
        'orders': orders,
    }
    return render(request, 'pages/orders/index.html', context)

@login_required
@permission_required('base.add_order', raise_exception=True)
@transaction.atomic
def addOrder(request):
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        order_product_forms = [OrderProductForm(request.POST, prefix=str(x)) for x in range(0, int(request.POST.get('form-TOTAL_FORMS', 1)))]
        
        if order_form.is_valid() and all([form.is_valid() for form in order_product_forms]):
            order = order_form.save(commit=False)
            order.addedBy = request.user
            order.updatedBy = request.user
            order.save()
            
            for form in order_product_forms:
                order_product = form.save(commit=False)
                order_product.order = order
                order_product.save()
            
            messages.success(
                request, 
                _("The order '%(order)s' has been created successfully.") % {'order': order.orderId}
            )
            return redirect(reverse('base:getOrders'))
        else:
            messages.error(request, _("Please correct the errors below and try again."))
    else:
        order_form = OrderForm()
        order_product_forms = [OrderProductForm(prefix='0')]
    
    context = {
        'order_form': order_form,
        'order_product_forms': order_product_forms,
        'title': _('Add New Order'),
    }
    return render(request, 'pages/orders/create.html', context)