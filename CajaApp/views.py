from django.shortcuts import render, redirect, get_object_or_404
from loginApp.models import Cajas, Empleados, Ventas
from django.db.models import Max
from django.utils import timezone
from django.contrib import messages

def caja_view(request):
    cajas = Cajas.objects.all().order_by('-id_caja')

    context = {
        'cajas': cajas,
    }
    return render(request, 'caja.html', context)


def detalle_caja_view(request, caja_id):
    caja = get_object_or_404(Cajas, id_caja=caja_id)

    # Si la caja está cerrada, usar la fecha de cierre
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
    
