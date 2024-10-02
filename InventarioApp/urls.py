from django.urls import path
from . import views

urlpatterns = [
    path('inventario/', views.inventario, name='inventario'),
    path('inventario/nuevo_registro/', views.nuevo_registro, name='nuevo_registro'),
    path('inventario/editar_producto/<int:producto_id>/', views.editar_producto, name='editar_producto'),
    path('inventario/borrar_producto/<int:producto_id>/', views.borrar_producto, name='borrar_producto'),
]
