from django.shortcuts import render
from loginApp.models import Ventas, Productos

def ventas_view(request):
    ventas = Ventas.objects.all()
    context = {
        'ventas': ventas,
    }
    return render(request, 'ventas.html', context)

def nueva_venta_view(request):
    productos = Productos.objects.all().order_by('-id_productos')
    context = {
        'productos': productos
    }
    return render(request, 'nueva_venta.html', context)
