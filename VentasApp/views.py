from django.shortcuts import render, redirect,get_object_or_404
from django.http import JsonResponse
from django.db import transaction
from django.db.models import Max, Sum
from django.core.exceptions import ValidationError
from loginApp.models import Ventas, Productos, Facturas, DetalleVentas, Clientes, Cajas
from django.utils import timezone
from django.contrib import messages
from decimal import Decimal
from django.db import connection



def nueva_venta_view(request):
    if not Cajas.objects.filter(estado_caja="Abierta").exists():
        messages.error(request, "Necesita abrir la caja para hacer una venta.")
        return redirect('ventas')
    
    id_venta = Ventas.objects.aggregate(Max('id_venta'))['id_venta__max'] or 1
    id_factura = Facturas.objects.aggregate(Max('id_factura'))['id_factura__max'] or 1
    id_caja = Cajas.objects.aggregate(Max('id_caja'))['id_caja__max'] or 1

    productos = Productos.objects.all().order_by('-id_productos')

    if request.method == 'POST':
        with transaction.atomic():
            try:
                nombre_cli = request.POST.get('nombre_cli')
                apellido_cli = request.POST.get('apellido_cli')
                dni = request.POST.get('dni')
                telefono = request.POST.get('telefono')

                if not nombre_cli or not apellido_cli or not dni or not telefono:
                    return JsonResponse({"success": False, "error": "Todos los campos del cliente son obligatorios."})

                nuevo_cliente = Clientes(nombre_cli=nombre_cli, apellido_cli=apellido_cli, dni=dni, telefono=telefono)
                nuevo_cliente.full_clean()
                nuevo_cliente.save()

                metodo_pago = request.POST.get('metodo_pago')
                total = request.POST.get('total')
                descuento = request.POST.get('descuento')

                nueva_factura = Facturas(id_clientes=nuevo_cliente, total=total, descuento=descuento, metodo_pago=metodo_pago)
                nueva_factura.full_clean()
                nueva_factura.save()

                caja_instance = Cajas.objects.get(id_caja=id_caja)

                nueva_venta = Ventas(
                    id_venta=id_venta + 1,
                    id_caja=caja_instance,
                    fecha_venta=timezone.now()
                )
                nueva_venta.full_clean()
                nueva_venta.save()

                detalles_venta = []
                for producto_data in request.POST.getlist('id_prod'):
                    cantidad = request.POST.get(f'cant_prod_vendido_{producto_data}')
                    
                    if cantidad is None:
                        return JsonResponse({"success": False, "error": f"La cantidad para el producto {producto_data} no está disponible."})
                    
                    cantidad = int(cantidad)
                    producto = Productos.objects.get(id_productos=producto_data)

                    subtotal = float(producto.precio_unitario_venta) * cantidad

                    if producto.cantidad_producto < cantidad:
                        return JsonResponse({"success": False, "error": f"No hay suficiente stock para el producto {producto.nombre}."})

                    detalle = DetalleVentas(
                        id_venta=nueva_venta,
                        id_factura=nueva_factura,
                        id_prod=producto,
                        cant_prod_vendido=cantidad,
                        subtotal=subtotal
                    )
                    detalles_venta.append(detalle)

                DetalleVentas.objects.bulk_create(detalles_venta)

                return redirect('ventas')

            except ValidationError as e:
                return JsonResponse({"success": False, "error": str(e)})
            except Exception as e:
                return JsonResponse({"success": False, "error": f"Error al guardar los datos: {e}"})

    context = {
        'id_venta': id_venta,
        'id_factura': id_factura,
        'id_caja': id_caja,
        'productos': productos
    }
    return render(request, 'nueva_venta.html', context)

def ventas_view(request):
    ventas = Facturas.objects.select_related('id_clientes').all()
    cajas = Cajas.objects.all()

    estado_caja_abierta = cajas.filter(estado_caja="Abierta").exists()
    
    context = {
        'ventas': ventas,
        'cajas': cajas,
        'estado_caja_abierta': estado_caja_abierta,
    }
    return render(request, 'ventas.html', context)



def detalle_venta_view(request, id_venta):
    
    with connection.cursor() as cursor:
        cursor.callproc('VerVenta', [id_venta])
        result = cursor.fetchall()
    
    detalles_venta = []
    for row in result:
        detalles_venta.append({
           "id_venta": row[0],
           "fecha_venta": row[1],
           "total_factura": (row[2] - row[3]),
           "descuento_factura": row[3],
           "metodo_pago": row[4],
           "id_clientes": row[5],
        })
        
    venta= get_object_or_404(Ventas, id_venta=id_venta)
  
    cliente= Facturas.objects.select_related("id_clientes").filter(id_factura=venta.id_venta).first()

    caja= Cajas.objects.all()

    productos= DetalleVentas.objects.filter(id_venta=venta)

    context= {
        "detalles_venta": detalles_venta,
        "venta": venta,
        "caja": caja,
        "cliente": cliente,
        "productos": productos,
    }    
    return render(request, 'detalle_venta.html', context)



"""def detalle_venta_view(request, id_venta):
    # Recupera la venta
    venta = get_object_or_404(Ventas, id_venta=id_venta)
        
    cliente = Facturas.objects.select_related('id_clientes').all() # Aquí accedes al cliente desde la factura
    
    caja = Cajas.objects.all()
    # Recupera los detalles de la venta (productos vendidos)
    productos = DetalleVentas.objects.filter(id_venta=venta)

    # Contexto para la plantilla
    context = {
        'venta': venta,
        "caja": caja,
        'cliente': cliente,
        'productos': productos,
    }
    
    return render(request, 'detalle_venta.html', context)
"""