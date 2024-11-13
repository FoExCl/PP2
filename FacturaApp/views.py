from django.shortcuts import render

# Create your views here.

def factura_view(request):
    return render(request, 'factura.html')