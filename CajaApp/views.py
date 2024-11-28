from django.shortcuts import render, redirect, get_object_or_404
from loginApp.models import Cajas, Empleados, Ventas, DetalleVentas
from django.db.models import Max, Prefetch,F, Value
from django.utils import timezone
from django.http import JsonResponse
from django.contrib import messages
from django.db.models.functions import Concat

def caja_view(request):
    cajas = Cajas.objects.all().order_by('-id_caja')

    context = {
        'cajas': cajas,
    }
    return render(request, 'caja.html', context)


def detalle_caja_view(request, caja_id):
    caja = get_object_or_404(Cajas, id_caja=caja_id)
    fecha_cierre = caja.fechacierrecaja or timezone.now()
    ventas_data = (
        Ventas.objects
        .filter(
            id_caja=caja,
            fecha_venta__gte=caja.fechaaperturacaja,
            fecha_venta__lte=fecha_cierre
        )
        .select_related('id_caja')
        .prefetch_related(
            Prefetch(
                'detalleventas_set',
                queryset=DetalleVentas.objects.select_related('id_factura__id_clientes')
            )
        )
    )

    data = []
    total_ventas = 0
    total_vuelto = 0
    for venta in ventas_data:
        detalle_venta = venta.detalleventas_set.first()
        if detalle_venta and detalle_venta.id_factura:
            factura = detalle_venta.id_factura
            cliente = factura.id_clientes

            venta_data = {
                'id_venta': venta.id_venta,
                'fecha_venta': venta.fecha_venta.strftime('%Y-%m-%d %H:%M:%S'),
                'total': float(factura.total) if factura.total else 0,
                'cliente': f"{cliente.nombre_cli or ''} {cliente.apellido_cli or ''}".strip(),
                'descuento': float(factura.descuento) if factura.descuento else 0,
                'metodo_pago': factura.metodo_pago,
                'vuelto': float(factura.vuelto) if factura.vuelto else 0
            }
            
            data.append(venta_data)
            
            total_ventas += venta_data['total']
            total_vuelto += venta_data['vuelto']

    context = {
        'caja': caja,
        'ventas': data,
        'monto_inicial': float(caja.monto_inicial) if caja.monto_inicial else 0,
        'total_ventas': total_ventas,
        'total_vuelto': total_vuelto
    }
    return render(request, 'detalle_caja.html', context)

def cerrar_caja_view(request, caja_id):
    caja = get_object_or_404(Cajas, id_caja=caja_id)

    if request.method == 'POST' and caja.estado_caja == 'Abierta':
        fecha_cierre = timezone.now()
        ventas_data = Ventas.objects.filter(
            id_caja=caja,
            fecha_venta__gte=caja.fechaaperturacaja,
            fecha_venta__lte=fecha_cierre
        )

        total_ventas = 0
        total_vuelto = 0
        for venta in ventas_data:
            factura = venta.detalleventas_set.first().id_factura if venta.detalleventas_set.exists() else None
            if factura:
                total_ventas += float(factura.total or 0)
                total_vuelto += float(factura.vuelto or 0)
        
        caja.estado_caja = 'Cerrada'
        caja.fechacierrecaja = fecha_cierre
        caja.total_ingresos_caja = total_ventas
        caja.total_egresos_caja = total_vuelto
        caja.save()

        return redirect('caja')

def apertura_view(request):
    caja_abierta = Cajas.objects.filter(estado_caja="Abierta").exists()
    
    if caja_abierta:
        messages.error(request, "Ya existe una caja abierta. Por favor, cierra la caja actual antes de abrir una nueva.")
        return redirect('caja')

    if request.method == 'POST':
        fechaaperturacaja = timezone.now()
        dni = Empleados.objects.get(dni=request.POST.get('dni'))
        monto_inicial = request.POST.get('monto_inicial')

        abrir_caja = Cajas(
            fechaaperturacaja=fechaaperturacaja,
            dni=dni,
            estado_caja="Abierta",
            total_ingresos_caja=0,
            monto_inicial=monto_inicial,
            total_egresos_caja=0,
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