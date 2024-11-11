from django import forms
from .models import Empleados, AuthUser, AuthGroup, AuthUserGroups
from django.contrib.auth.hashers import make_password  
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError  
from django.utils import timezone

class EmpleadoCreationForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True, label="Nombre de usuario")
    password1 = forms.CharField(widget=forms.PasswordInput, required=True, label="Contraseña")
    password2 = forms.CharField(widget=forms.PasswordInput, required=True, label="Confirmar contraseña")
    group_name = 'Empleado'

    class Meta:
        model = Empleados
        fields = ['nombre', 'apellido', 'edad', 'telefono', 'correo', 'direccion']

    def clean_correo(self):
        correo = self.cleaned_data['correo']
        if AuthUser.objects.filter(email=correo).exists():
            raise ValidationError('Este correo electrónico ya está registrado.')
        return correo

    def clean_username(self):
        username = self.cleaned_data['username']
        if AuthUser.objects.filter(username=username).exists():
            raise ValidationError('Este nombre de usuario ya está registrado.')
        return username

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("Las contraseñas no coinciden.")

    def save(self, commit=True):
        username = self.cleaned_data['username']
        password = make_password(self.cleaned_data['password1'])  
        correo = self.cleaned_data['correo']
        first_name = self.cleaned_data['nombre']
        last_name = self.cleaned_data['apellido']

        user = AuthUser(
            username=username,
            email=correo,
            first_name=first_name,
            last_name=last_name,
            is_active=1,
            is_staff=0,
            is_superuser=0,
            password=password,
            date_joined=timezone.now()
        )
        user.save()

        empleado = super().save(commit=False)
        empleado.id_user = user

        if commit:
            empleado.save()

        grupo_empleado, created = AuthGroup.objects.get_or_create(name=self.group_name)
        AuthUserGroups.objects.create(user=user, group=grupo_empleado)

        return empleado
    

class EditarEmpleadoForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True, label="Nombre de usuario")
    class Meta:
        model = Empleados
        fields = ['nombre', 'apellido', 'edad', 'telefono', 'correo', 'direccion']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.id_user:
            self.fields['username'].initial = self.instance.id_user.username
            self.fields['nombre'].initial = self.instance.id_user.first_name
            self.fields['apellido'].initial = self.instance.id_user.last_name
            self.fields['correo'].initial = self.instance.id_user.email

    def clean_correo(self):
        correo = self.cleaned_data['correo']
        if AuthUser.objects.filter(email=correo).exclude(id=self.instance.id_user.id).exists():
            raise forms.ValidationError('Este correo electrónico ya está registrado por otro usuario.')
        return correo

    def save(self, commit=True):
        empleado = super().save(commit=False)
        user = empleado.id_user

        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['nombre']
        user.last_name = self.cleaned_data['apellido']
        user.email = self.cleaned_data['correo']

        if commit:
            user.save()
            empleado.save()

        return empleado