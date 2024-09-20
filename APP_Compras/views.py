from django.shortcuts import render,redirect
from loginApp.models import Compras, Provxprod,Cajas

# Create your views here.
def registro_Prov(request):
    # Prov= Proveedores
    Prov=Proveedores.objects.all()
    return render(request, "carga_Compra.html", {"Prov=Prov"})

def home(request):
    return render(request, "index.html")

def prueba(request):
    return render(request, "prueba1.html")

def registro_Compra(request):
    id_compra=request.POST["txtID"]
    id_provxprod=request.POST["txtID_Proveedor"]
    id_caja=request.POST["txtID_Caja"]
    Cantidad=request.POST["numCantidad"]
    Precio_Total=request.POST["num_Total_Compra"]
    Compra=Compras.objects.create(id_compra=id_compra, Cantidad=Cantidad, Precio_Total=Precio_Total)
    Prov=Provxprod.objects.create(id_provxprod=id_provxprod)
    caja=Cajas.objects.create(id_caja=id_caja)


def registro_Prov(request):
    # Prov= Proveedores
    Prov=Provxprod.objects.all()
    return render(request, "carga_Compra.html", {"Prov=prod"})

def eliminar(request):

def modificar(request):
