from django.shortcuts import render
from loginApp.models import cajas,empleados
# Create your views here.

def home(request):
    return render(request,"home.html")

