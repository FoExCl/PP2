import json
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Count
from django.db.models.functions import TruncMonth,TruncWeek
from django.utils.translation import activate
from loginApp.models import Ventas, Productos, Facturas, DetalleVentas, Cajas
from django.db.models import Count, Sum


def ChartData(request):
    activate('es')

    ventas_por_mes = (
        Ventas.objects.annotate(mes=TruncMonth('fecha_venta'))
        .values('mes')
        .annotate(cantidad=Count('id_venta'))
        .order_by('mes')
    )

    etiquetas = [venta["mes"].strftime("%B") for venta in ventas_por_mes]
    datos = [venta["cantidad"] for venta in ventas_por_mes]

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            "labels": etiquetas,
            "data": datos,
        })

    context = {
        "labels": json.dumps(etiquetas),  
        "data": json.dumps(datos),       
        "chartLabel": "Ventas realizadas por Mes",
    }
    return render(request, 'grafico1.html', context)

def chart_data1(request):
    chart_label = "Productos Más Vendidos"
    etiquetas = []  # Nombres de los productos
    datos = []  # Cantidades vendidas

    # Agrupar las ventas por producto
    productos_vendidos = (
        DetalleVentas.objects
        .values('id_prod')  # Agrupar por ID de producto
        .annotate(total_vendido=Sum('cant_prod_vendido'))  # Sumar cantidad vendida
        .order_by('-total_vendido')  # Ordenar por cantidad vendida en orden descendente
    )

    # Recuperar los nombres de los productos
    for producto in productos_vendidos:
        producto_obj = Productos.objects.get(id_productos=producto['id_prod'])
        etiquetas.append(producto_obj.tipo_prod)  # Nombre del producto
        datos.append(producto['total_vendido'])  # Cantidad vendida

    # Contexto para el gráfico
    context = {
        "labels": etiquetas,  # Nombres de los productos
        "chartLabel": chart_label,  # Etiqueta del gráfico
        "data": datos,  # Cantidades vendidas
    }

    return render(request, 'grafico1.html', context)

def combined_charts(request):
    activate('es')

    # Datos para el gráfico de barras (Ventas por Mes)
    ventas_por_mes = (
        Ventas.objects.annotate(mes=TruncMonth('fecha_venta'))
        .values('mes')
        .annotate(cantidad=Count('id_venta'))
        .order_by('mes')
    )
    etiquetas_barras = [venta["mes"].strftime("%B") for venta in ventas_por_mes]
    datos_barras = [venta["cantidad"] for venta in ventas_por_mes]

    # Datos para el gráfico de torta (Productos Más Vendidos)
    etiquetas_torta = []  # Nombres de los productos
    datos_torta = []  # Cantidades vendidas

    productos_vendidos = (
        DetalleVentas.objects
        .values('id_prod')  # Agrupar por ID de producto
        .annotate(total_vendido=Sum('cant_prod_vendido'))  # Sumar cantidad vendida
        .order_by('-total_vendido')  # Ordenar por cantidad vendida en orden descendente
    )

    for producto in productos_vendidos:
        producto_obj = Productos.objects.get(id_productos=producto['id_prod'])
        etiquetas_torta.append(producto_obj.tipo_prod)  # Nombre del producto
        datos_torta.append(producto['total_vendido'])  # Cantidad vendida

    # Contexto combinado
    context = {
        "labels_barras": json.dumps(etiquetas_barras),  # Etiquetas para gráfico de barras
        "data_barras": json.dumps(datos_barras),  # Datos para gráfico de barras
        "chartLabelBarras": "Ventas realizadas por Mes",
        "labels_torta": json.dumps(etiquetas_torta),  # Etiquetas para gráfico de torta
        "data_torta": json.dumps(datos_torta),  # Datos para gráfico de torta
        "chartLabelTorta": "Productos Más Vendidos",
    }

    return render(request, 'grafico1.html', context)