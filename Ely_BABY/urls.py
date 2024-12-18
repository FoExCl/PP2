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
from django.urls import path, include, reverse_lazy
from loginApp import views
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.combined_charts, name='home'),
    path('inicio/', views.inicio, name='inicio'),
    path('signin/', views.signin, name='signin'),

    path('users/', views.user_list, name='userlist'),
    path('users/add/', views.add_user, name='add_user'),
    path('users/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('user/edit/<int:user_id>/', views.edit_profile, name='edit_profile'),
    path('user/change-password/', views.change_password, name='change_password'),
    path('users/toggle-active/<int:user_id>/', views.toggle_user_active, name='toggle_user_active'),
    

    path('user/', views.user_profile, name='user'),
    
    path('logout/', views.exit, name='exit'),
    path('inventario/', include('InventarioApp.urls')),
    path('caja/', include('CajaApp.urls')),
    path('ventas/', include('VentasApp.urls')),
    path("graficos/", include("GraficosApp.urls")),

    path('password_reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='password_reset.html',
             email_template_name='password_reset_email.html',
             subject_template_name='password_reset_subject.txt',
             success_url=reverse_lazy('password_reset_done')
         ),
         name='password_reset'),
    
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='password_reset_done.html'
         ),
         name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='password_reset_confirm.html',
             success_url=reverse_lazy('password_reset_complete')
         ),
         name='password_reset_confirm'),
    
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='password_reset_complete.html'
         ),
         name='password_reset_complete'),
]
    