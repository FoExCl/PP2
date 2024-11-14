from django.shortcuts import render, redirect, get_object_or_404
from loginApp.models import Cajas, Empleados, Ventas, DetalleVentas
from django.db.models import Max,  Prefetch
from django.utils import timezone
from django.http import JsonResponse
from django.contrib import messages

def caja_view(request):
    cajas = Cajas.objects.all().order_by('-id_caja')

    context = {
        'cajas': cajas,
    }
    return render(request, 'caja.html', context)


def detalle_caja_view(request, caja_id):
    caja = get_object_or_404(Cajas, id_caja=caja_id)

    if caja.fechacierrecaja:
        fecha_cierre = caja.fechacierrecaja
    else:
        fecha_cierre = timezone.now()
        
    ventas = Ventas.objects.filter(
        fecha_venta__gte=caja.fechaaperturacaja,
        fecha_venta__lte=fecha_cierre
    )

    context = {
        'caja': caja,
        'ventas': ventas
    }
    return render(request, 'detalle_caja.html', context)

def cerrar_caja_view(request, caja_id):
    caja = get_object_or_404(Cajas, id_caja=caja_id)

    if request.method == 'POST' and caja.estado_caja == 'Abierta':
        caja.estado_caja = 'Cerrada'
        caja.fechacierrecaja = timezone.now()
        caja.save()

        return redirect('caja')
    
def get_ventas_data(request):
    caja_id = request.GET.get('caja_id')
    caja = get_object_or_404(Cajas, id_caja=caja_id)
    fecha_cierre = caja.fechacierrecaja if caja.estado_caja == 'Cerrada' else timezone.now()
    
    ventas_data = (
        Ventas.objects
        .select_related('id_caja')
        .prefetch_related(
            Prefetch(
                'detalleventas_set',
                queryset=DetalleVentas.objects.select_related('id_factura__id_clientes')
            )
        )
        .filter(
            fecha_venta__gte=caja.fechaaperturacaja,
            fecha_venta__lte=fecha_cierre
        )
        .values(
            'id_venta',
            'fecha_venta',
            'detalleventas__id_factura__total',
            'detalleventas__id_factura__id_clientes__nombre_cli',
            'detalleventas__id_factura__id_clientes__apellido_cli',
            'detalleventas__id_factura__descuento',
            'detalleventas__id_factura__metodo_pago'
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
            'metodo_pago': venta['detalleventas__id_factura__metodo_pago']
        })

    return JsonResponse({'data': data})

def apertura_view(request):
    caja_abierta = Cajas.objects.filter(estado_caja="Abierta").exists()
    
    if caja_abierta:
        messages.error(request, "Ya existe una caja abierta. Por favor, cierra la caja actual antes de abrir una nueva.")
        return redirect('caja')

    if request.method == 'POST':
        fechaaperturacaja = timezone.now()
        dni = Empleados.objects.get(dni=request.POST.get('dni'))
        total_egresos_caja = request.POST.get('total_egresos_caja')

        abrir_caja = Cajas(
            fechaaperturacaja=fechaaperturacaja,
            dni=dni,
            estado_caja="Abierta",
            total_ingresos_caja=0,
            total_egresos_caja=total_egresos_caja,
            fechacierrecaja=timezone.datetime(9999, 12, 31)
        )
        abrir_caja.save()

        return redirect('caja')

    max_caja_id = Cajas.objects.all().aggregate(Max('id_caja'))['id_caja__max']
    next_caja_id = max_caja_id + 1 if max_caja_id is not None else 1

    empleados = Empleados.objects.all()
    current_time = timezone.now().strftime('%Y-%m-%d %H:%M:%S')

    return render(request, 'apertura.html', {
        'next_caja_id': next_caja_id, 
        'empleados': empleados, 
        'current_time': current_time
    })
    
    