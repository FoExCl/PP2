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
from InventarioApp.views import inventario_view, nuevo_registro_view, editar_producto_view, borrar_producto_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('Compras/', include("APP_Compras.urls")),
    path('', views.home, name='home'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('users/', views.user_list, name='userlist'),
    path('user/', views.user_profile, name='user'),
    path('logout/', views.exit, name='exit'),
    path('inventario/', inventario_view, name='inventario'),
    path('inventario/nuevo_registro/', nuevo_registro_view, name='nuevo_registro'),
    path('inventario/editar_producto/<int:producto_id>/', editar_producto_view, name='editar_producto'),
    path('inventario/borrar_producto/<int:producto_id>/', borrar_producto_view, name='borrar_producto'),
     
]
