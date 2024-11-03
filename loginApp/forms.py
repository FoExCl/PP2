from django import forms
from loginApp.models import AuthUser

class AddUserForm(forms.ModelForm):
    class Meta:
        model = AuthUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'is_superuser', 'is_staff', 'is_active')
        labels = {
            'username': 'Nombre de Usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo Electrónico',
            'password': 'Contraseña',
            'is_superuser': 'Es Administrador',
            'is_staff': 'Es Staff',
            'is_active': 'Está Activo',
        }
        widgets = {
            'password': forms.PasswordInput(),
        }


class EditarUsuarioForm(forms.ModelForm):
    class Meta:
        model = AuthUser
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
            'username': 'Nombre de Usuario:',
            'first_name': 'Nombre:',
            'last_name': 'Apellido:',
            'email': 'Email:',
            
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese nombre de usuario', 'readonly': 'readonly'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese nombre'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese apellido'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese correo electrónico'}),
        }
