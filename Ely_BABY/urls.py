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
from django.contrib.auth.decorators import login_required, user_passes_test


admin.site.login = login_required(user_passes_test(lambda u: u.is_superuser)(admin.site.login))
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),

    path('users/', views.user_list, name='userlist'),
    path('users/add/', views.add_user, name='add_user'),
    path('users/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    
    path('user/', views.user_profile, name='user'),
    
    path('logout/', views.exit, name='exit'),
    path('inventario/', include('InventarioApp.urls')),
    path('caja/', include('CajaApp.urls')),
    path('ventas/', include('VentasApp.urls'))
]
    
