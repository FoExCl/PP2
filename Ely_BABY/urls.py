"""
URL configuration for elybaby project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from loginApp import views
from VentasApp.views import nueva_venta_view
from django.contrib.auth.decorators import login_required, user_passes_test


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('inicio/', views.inicio, name='inicio'),
    path('signin/', views.signin, name='signin'),

    path('users/', views.user_list, name='userlist'),
    path('users/add/', views.add_user, name='add_user'),
    path('users/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('users/toggle-active/<int:user_id>/', views.toggle_user_active, name='toggle_user_active'),

    path('user/', views.user_profile, name='user'),
    
    path('logout/', views.exit, name='exit'),
    path('inventario/', include('InventarioApp.urls')),
    path('caja/', include('CajaApp.urls')),
    path('nueva_venta/', nueva_venta_view, name='nueva_venta'),
    path('ventas/', include('VentasApp.urls'))
]
    