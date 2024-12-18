from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db import transaction, connection
from django.db.models import Max, F, Prefetch
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
                vuelto = request.POST.get('vuelto', '0')  # Add vuelto field, default to 0 if not provided

                nueva_factura = Facturas(
                    id_clientes=nuevo_cliente, 
                    total=total, 
                    descuento=descuento, 
                    metodo_pago=metodo_pago,
                    vuelto=vuelto  # Add vuelto to the Facturas model
                )
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

                    producto.cantidad_producto -= cantidad
                    producto.save()

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
    estado_caja_abierta = True
    
    return render(request, 'ventas.html', {
        'estado_caja_abierta': estado_caja_abierta
    })

def get_ventas_data(request):
    ventas_data = (
        Ventas.objects
        .select_related('id_caja')
        .prefetch_related(
            Prefetch(
                'detalleventas_set',
                queryset=DetalleVentas.objects.select_related('id_factura__id_clientes')
            )
        )
        .values(
            'id_venta',
            'fecha_venta',
            'detalleventas__id_factura__total',
            'detalleventas__id_factura__id_clientes__nombre_cli',
            'detalleventas__id_factura__id_clientes__apellido_cli',
            'detalleventas__id_factura__descuento',
            'detalleventas__id_factura__metodo_pago',
            'detalleventas__id_factura__vuelto'  # Add this line to include vuelto
        )
        .distinct()
    )

    data = []
    for venta in ventas_data:
        data.append({
            'id_venta': venta['id_venta'],
            'fecha_venta': venta['fecha_venta'].strftime('%Y-%m-%d %H:%M:%S'),
            'total': float(venta['detalleventas__id_factura__total']) if venta['detalleventas__id_factura__total'] else 0,
            'cliente': f"{venta['detalleventas__id_factura__id_clientes__nombre_cli']} {venta['detalleventas__id_factura__id_clientes__apellido_cli']}".strip(),
            'descuento': float(venta['detalleventas__id_factura__descuento']) if venta['detalleventas__id_factura__descuento'] else 0,
            'metodo_pago': venta['detalleventas__id_factura__metodo_pago'],
            'vuelto': float(venta['detalleventas__id_factura__vuelto']) if venta['detalleventas__id_factura__vuelto'] else 0  # Add this line
        })

    return JsonResponse({'data': data})

def detalle_venta_view(request, id_venta):

    venta = get_object_or_404(Ventas, id_venta=id_venta)
    with connection.cursor() as cursor:
        cursor.callproc('VerVenta', [id_venta])
        #cursor.callproc('VerVenta', [id_factura])
        result = cursor.fetchall()

    detalles_venta = [
        {
            "id_venta": row[0],
            "fecha_venta": row[1],
            "total_factura": row[2],
            "descuento_factura": row[3],
            "metodo_pago": row[4],
            "vuelto": row[5],  #campo "vuelto"
            "id_clientes": row[6],
        }
        for row in result
    ]

    if not detalles_venta:
        return JsonResponse({"error": "No se encontraron detalles para esta venta."})

    cliente_id = detalles_venta[0]["id_clientes"]
    cliente = Clientes.objects.filter(id_clientes=cliente_id).first()

    caja = Cajas.objects.filter(id_caja=venta.id_caja.id_caja).first()

    productos = DetalleVentas.objects.filter(id_venta=venta).select_related('id_prod')

    context = {
        "detalles_venta": detalles_venta,
        "venta": venta,
        "caja": caja,
        "cliente": cliente,
        "productos": productos,
    }
    return render(request, 'detalle_venta.html', context)