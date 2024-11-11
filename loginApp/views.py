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



def home(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')
    else:
        return redirect('signin')


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm()
        })
    else:
        try:
            if request.POST['password1'] == request.POST['password2']:
                user = User.objects.create_user(
                    username=request.POST['usuario'], 
                    password=request.POST['password1'],
                    first_name=request.POST['nombre'],
                    last_name=request.POST['apellido'],
                    email=request.POST['correo']
                )

                if request.POST['user_type'] == 'admin':
                    user.is_superuser = True
                    user.is_staff = True
                else:
                    user.is_superuser = False
                    user.is_staff = False

                user.save()
                return redirect('userlist')
            else:
                return render(request, 'signup.html', {
                    'form': UserCreationForm(),
                    'error': 'Passwords do not match'
                })
        except KeyError as e:
            return render(request, 'signup.html', {
                'form': UserCreationForm(),
                'error': f'Missing field: {str(e)}'
            })
        except IntegrityError:
            return render(request, 'signup.html', {
                'form': UserCreationForm(),
                'error': 'User already exists'
            })


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
    empleados = Empleados.objects.all()
    return render(request, 'userlist.html', {'empleados': empleados})




@login_required
def add_user(request):
    if request.method == 'POST':
        form = EmpleadoCreationForm(request.POST)
        if form.is_valid():
            form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            messages.success(request, "El usuario ha sido creado correctamente.")
            return redirect('userlist')
    else:
        form = EmpleadoCreationForm()
    
    return render(request, 'add_user.html', {'form': form})

@login_required
def edit_user(request, user_id):
    empleado = get_object_or_404(Empleados, id_user__id=user_id)

    if request.method == 'POST':
        form = EditarEmpleadoForm(request.POST, instance=empleado)
        if form.is_valid():
            form.save()
            messages.success(request, "El usuario ha sido actualizado correctamente.")
            return redirect('userlist')
    else:
        form = EditarEmpleadoForm(instance=empleado)

    return render(request, 'edit_user.html', {'form': form, 'empleado': empleado})

@login_required
def delete_user(request, user_id):
    empleado = get_object_or_404(Empleados, id_user__id=user_id)
    user = empleado.id_user

    try:
        with transaction.atomic():
            AuthUserGroups.objects.filter(user=user).delete()
            AuthUserUserPermissions.objects.filter(user=user).delete()
            empleado.delete()
            AuthUser.objects.filter(id=user.id).delete()
        
        messages.success(request, "El usuario ha sido eliminado permanentemente.")
    except Exception as e:
        messages.error(request, f"Error al eliminar el usuario: {str(e)}")

    return redirect('userlist')