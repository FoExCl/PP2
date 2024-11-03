from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render
from loginApp.models import AuthUser
from loginApp.forms import AddUserForm, EditarUsuarioForm
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404


# Create your views here.
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
            return redirect('home')

def exit(request):
    logout(request)
    return redirect('signin')
        
#------------
def user_profile(request):
    return render(request, 'user.html', {
        'user': request.user  
    })

def user_list(request):
    if not request.user.is_authenticated:
        return redirect('signin')  # Redirige a la página de inicio de sesión si no está autenticado
    
    users = AuthUser.objects.all()
    for user in users:
        if user.is_superuser:
            user.role = "Administrador"  
        else: 
            user.role ="Vendedor"
    
    return render(request, 'userlist.html', {'users': users})

def add_user(request):
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "El usuario ha sido creado correctamente.")
            return redirect('userlist')
    else:
        form = AddUserForm()
    
    return render(request, 'add_user.html', {'form': form})


def edit_user(request, user_id):
    user = get_object_or_404(AuthUser, id=user_id)

    if request.method == 'POST':
        form = EditarUsuarioForm(request.POST, instance=user)
        if form.is_valid():
            user.username = form.cleaned_data['username']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            
            user.save()
            messages.success(request, "El usuario ha sido actualizado correctamente.")
            return redirect('userlist')
    else:
        form = EditarUsuarioForm(instance=user)

    return render(request, 'edit_user.html', {'form': form, 'user': user})



def delete_user(request, user_id):
    user = get_object_or_404(AuthUser, id=user_id)
    if request.user.id == user_id:
        messages.error(request, "No puedes eliminar tu propia cuenta.")
        return redirect('userlist')
    if request.method == 'POST':
        user.delete()  # Elimina el usuario
        messages.success(request, "El usuario ha sido eliminado correctamente.")
        return redirect('userlist')
    messages.error(request, "Error en la eliminación del usuario.")
    return redirect('userlist')