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
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)