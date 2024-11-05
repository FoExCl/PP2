from django.urls import path
from .views import factura_view

urlpatterns = [
    path('', factura_view, name='factura'),
]