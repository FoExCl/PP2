from django.urls import path
<<<<<<< HEAD
from .views import ventas_view, nueva_venta_view
=======
from .views import ventas_view, nueva_venta_view, detalle_venta_view
>>>>>>> afe2c0df60800fffe0bbe8016e12ce4de7a1958a

urlpatterns = [
    path('', ventas_view, name='ventas'),
    path('nueva_venta/', nueva_venta_view, name='nueva_venta'),
]