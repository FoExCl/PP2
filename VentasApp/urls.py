from django.urls import path
from .views import ventas_view, get_ventas_data, detalle_venta_view

urlpatterns = [
    path('', ventas_view, name='ventas'),
    path('get_ventas_data/', get_ventas_data, name='get_ventas_data'),
    path('detalle_venta/<int:id_venta>/', detalle_venta_view, name='detalle_venta'),
]