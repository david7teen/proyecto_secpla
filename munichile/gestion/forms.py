from django import forms
from django.contrib.auth.models import User
from registration.models import Profile
from .models import *

class UsuarioForm(forms.ModelForm):
    telefono = forms.CharField(max_length=20, required=True)
    perfil = forms.ChoiceField(choices=Profile.PERFIL_CHOICES, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            profile, created = Profile.objects.get_or_create(user=user)
            profile.telefono = self.cleaned_data["telefono"]
            profile.perfil = self.cleaned_data["perfil"]
            profile.save()
        return user

class UsuarioEditForm(forms.ModelForm):
    telefono = forms.CharField(max_length=20, required=True)
    perfil = forms.ChoiceField(choices=Profile.PERFIL_CHOICES, required=True)
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            profile = self.instance.profile
            self.fields['telefono'].initial = profile.telefono
            self.fields['perfil'].initial = profile.perfil
    
    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            profile = user.profile
            profile.telefono = self.cleaned_data["telefono"]
            profile.perfil = self.cleaned_data["perfil"]
            profile.save()
        return user

class DireccionForm(forms.ModelForm):
    class Meta:
        model = Direccion
        fields = ["nombre_direccion", "nombre_encargado", "correo_encargado", "state"]

class DepartamentoForm(forms.ModelForm):
    class Meta:
        model = Departamento
        fields = ["direccion", "nombre_departamento", "nombre_encargado", "correo_encargado", "state"]

class TipoIncidenciaForm(forms.ModelForm):
    class Meta:
        model = TipoIncidencia
        fields = ["departamento", "nombre", "descripcion", "state"]

class CuadrillaForm(forms.ModelForm):
    class Meta:
        model = Cuadrilla
        fields = ["nombre_cuadrilla", "departamento", "state"]

class EncuestaForm(forms.ModelForm):
    class Meta:
        model = Encuesta
        fields = [
            "titulo", "descripcion", "ubicacion", "prioridad",
            "nombre_vecino", "celular_vecino", "correo_vecino", "direccion_vecino",
            "tipo_incidencia", "bloqueada", "state"
        ]
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }

class PreguntaForm(forms.ModelForm):
    class Meta:
        model = Pregunta
        fields = ["texto_pregunta", "tipo_respuesta", "orden", "opciones", "state"]
        widgets = {
            'texto_pregunta': forms.Textarea(attrs={'rows': 2}),
            'opciones': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Opción 1, Opción 2, Opción 3...'}),
        }

class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = ["encuesta", "descripcion", "ubicacion", "comuna", "estado", "prioridad"]
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
        }

class AsignarSolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = ["departamento_asignado", "cuadrilla_asignada", "estado"]

class ArchivoAdjuntoForm(forms.ModelForm):
    class Meta:
        model = ArchivoAdjunto
        fields = ["tipo", "ruta_archivo", "descripcion"]

class UsuarioCuadrillaForm(forms.ModelForm):
    class Meta:
        model = UsuarioCuadrilla
        fields = ["usuario", "cuadrilla"]
