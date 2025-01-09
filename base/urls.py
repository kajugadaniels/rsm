from django.urls import path
from base.views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = 'base'

urlpatterns = [
    path('dashboard/', dashboard, name="dashboard"),

    path('roles/', getRoles, name="getRoles"),
    path('role/add/', addRole, name="addRole"),
    path('role/edit/<slug>/', editRole, name="editRole"),
    path('role/delete/<slug>/', deleteRole, name="deleteRole"),

    path('products/', getProducts, name="getProducts"),
    path('product/add/', addProduct, name="addProduct"),
    path('product/edit/<slug>/', editProduct, name="editProduct"),
    path('product/delete/<slug>/', deleteProduct, name="deleteProduct"),

    path('clients/', getClients, name="getClients"),
    path('client/add/', addClient, name="addClient"),
    path('client/edit/<int:id>/', editClient, name="editClient"),
    path('client/delete/<int:id>/', deleteClient, name="deleteClient"),

    path('orders/', getOrders, name="getOrders"),
    path('order/add/', addOrder, name="addOrder"),
    path('order/edit/<str:orderId>/', editOrder, name="editOrder"),
    path('order/delete/<str:orderId>/', deleteOrder, name="deleteOrder"),
    path('order/<str:orderId>/', showOrder, name="showOrder"),
    path('order-product/delete/<int:id>/', deleteOrderProduct, name='deleteOrderProduct'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
