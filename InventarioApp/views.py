from django.shortcuts import render, get_object_or_404, redirect
from loginApp.models import Productos
from django.db.models import Max

def inventario_view(request):
    productos = Productos.objects.all().order_by('-id_productos')

    tipos_productos = Productos.objects.values_list('tipo_prod', flat=True).distinct()
    tipo_filtrado = request.GET.get('tipo_prod')
    if tipo_filtrado:
        productos = productos.filter(tipo_prod=tipo_filtrado)

    return render(request, 'inventario.html', {
        'productos': productos,
        'tipos_productos': tipos_productos,
        'tipo_filtrado': tipo_filtrado
    })

def nuevo_producto_view(request):
    if request.method == 'POST':
        tipo_prod = request.POST.get('tipo_prod')
        talle_prod = request.POST.get('talle_prod')
        color_prod = request.POST.get('color_prod')
        genero_prod = request.POST.get('genero_prod')
        precio_unitario_venta = request.POST.get('precio_unitario_venta')
        cantidad_producto = request.POST.get('cantidad_producto')
        descripcion = request.POST.get('descripcion')

        nuevo_producto = Productos(
            tipo_prod=tipo_prod,
            talle_prod=talle_prod,
            color_prod=color_prod,
            genero_prod=genero_prod,
            precio_unitario_venta=precio_unitario_venta,
            cantidad_producto=cantidad_producto,
            descripcion=descripcion
        )
        nuevo_producto.save()

        return redirect('inventario')

    max_id = Productos.objects.all().aggregate(Max('id_productos'))['id_productos__max']
    next_id = max_id + 1 if max_id is not None else 1

    return render(request, 'nuevo_producto.html', {'next_id': next_id})

def editar_producto_view(request, producto_id):
    producto = get_object_or_404(Productos, pk=producto_id)

    if request.method == 'POST':
        producto.tipo_prod = request.POST.get('tipo_prod')
        producto.talle_prod = request.POST.get('talle_prod')
        producto.color_prod = request.POST.get('color_prod')
        producto.genero_prod = request.POST.get('genero_prod')
        producto.precio_unitario_venta = request.POST.get('precio_unitario_venta')
        producto.cantidad_producto = request.POST.get('cantidad_producto')
        producto.descripcion = request.POST.get('descripcion')
        producto.save()
        return redirect('inventario')

    return render(request, 'editar_producto.html', {'producto': producto})

def borrar_producto_view(request, producto_id):
    producto = get_object_or_404(Productos, pk=producto_id)
    producto.delete()
    return redirect('inventario')
