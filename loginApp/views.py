from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render


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
        
#------------
def user_list(request):
    if not request.user.is_authenticated:
        return redirect('signin') 
    users = User.objects.all()
    for user in users:
        if user.is_superuser:
            user.role = "Administrador"
        else:
            user.role = "Vendedor"
    return render(request, 'userlist.html', {'users': users})

def exit(request):
    logout(request)
    return redirect('signin')