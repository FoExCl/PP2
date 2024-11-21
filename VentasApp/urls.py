from django.urls import path
from .views import ventas_view, nueva_venta_view, detalle_venta_view,ChartData

urlpatterns = [
    path('', ventas_view, name='ventas'),
    path('nueva_venta/', nueva_venta_view, name='nueva_venta'),
    path('detalle_venta/<int:id_venta>/', detalle_venta_view, name='detalle_venta'),
    path('chart-data/', ChartData, name='chart_data'),
]