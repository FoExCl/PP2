from django.urls import path
from . import views

urlpatterns = [
    path("registro/", views.registro_Prov),
    path("home/", views.home),
    path("prueba/", views.prueba)
    
]
