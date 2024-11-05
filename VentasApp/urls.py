from django.urls import path
from .views import ventas_view, nueva_venta_view

urlpatterns = [
    path('', ventas_view, name='ventas'),
    path('nueva_venta/', nueva_venta_view, name='nueva_venta'),
]