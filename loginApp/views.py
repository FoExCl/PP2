from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from loginApp.models import Empleados, AuthUser, AuthUserGroups, AuthUserUserPermissions
from loginApp.forms import EmpleadoCreationForm, EditarEmpleadoForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods




def home(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')
    else:
        return render('inicio.html')



def signin(request):
    if request.method == 'GET':
       return render(request, 'signin.html', {
            'form': AuthenticationForm
       })
    else: 
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
              return render(request, 'signin.html', {
                 'form': AuthenticationForm,
                 'error': 'Username or password is incorrect'
               })
        else:
            login(request, user)
            return redirect('user')


def exit(request):
    logout(request)
    return redirect('signin')


def user_profile(request):
    auth_user = get_object_or_404(AuthUser, username=request.user.username)
    empleado = get_object_or_404(Empleados, id_user=auth_user)
    return render(request, 'user.html', {'empleado': empleado})


@login_required
def user_list(request):
    empleados = Empleados.objects.all().select_related('id_user')
    return render(request, 'userlist.html', {'empleados': empleados})



@login_required
@require_http_methods(["GET", "POST"])
def add_user(request):
    if request.method == 'POST':
        form = EmpleadoCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            messages.success(request, f"El usuario {new_user.nombre} ha sido creado correctamente.")
            return JsonResponse({'success': True, 'message': f"El usuario {new_user.nombre} ha sido creado correctamente."})
        else:
            print(f"Form errors: {form.errors}")  # Add this line for debugging
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = EmpleadoCreationForm()
    
    return render(request, 'add_user.html', {'form': form})



@login_required
@require_http_methods(["GET", "POST"])
def edit_user(request, user_id):
    empleado = get_object_or_404(Empleados, id_user__id=user_id)
    if request.method == 'POST':
        form = EditarEmpleadoForm(request.POST, instance=empleado)
        if form.is_valid():
            updated_user = form.save()
            messages.success(request, f"El usuario {updated_user.nombre} ha sido actualizado correctamente.")
            return JsonResponse({'success': True, 'message': f"El usuario {updated_user.nombre} ha sido actualizado correctamente."})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = EditarEmpleadoForm(instance=empleado)
    return render(request, 'edit_user.html', {'form': form, 'empleado': empleado})



@login_required
@require_http_methods(["POST"])
def toggle_user_active(request, user_id):
    empleado = get_object_or_404(Empleados, id_user__id=user_id)
    user = empleado.id_user
    user.is_active = not user.is_active
    user.save()
    
    status = "activado" if user.is_active else "desactivado"
    messages.success(request, f"El usuario {empleado.nombre} ha sido {status}.")
    return JsonResponse({'success': True, 'is_active': user.is_active})