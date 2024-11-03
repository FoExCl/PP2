from django.urls import path
from .views import inventario_view, nuevo_producto_view, editar_producto_view, borrar_producto_view

urlpatterns = [
    path('', inventario_view, name='inventario'),
    path('nuevo_producto/', nuevo_producto_view, name='nuevo_producto'),
    path('editar_producto/<int:producto_id>/', editar_producto_view, name='editar_producto'),
    path('borrar_producto/<int:producto_id>/', borrar_producto_view, name='borrar_producto'),
]

