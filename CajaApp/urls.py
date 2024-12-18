from django.urls import path
from .views import apertura_view, caja_view, detalle_caja_view, cerrar_caja_view

urlpatterns = [
    path('', caja_view, name='caja'),
    path('apertura/', apertura_view, name='apertura'),
    path('detalle_caja/<int:caja_id>/', detalle_caja_view, name='detalle_caja'),
    path('cerrar/<int:caja_id>/', cerrar_caja_view, name='cerrar_caja'),
]