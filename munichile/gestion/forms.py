# gestion/forms.py
from django import forms
from .models import Encuesta, TipoIncidencia

class EncuestaForm(forms.ModelForm):
    
    # Hacemos que el combo de Tipo de Incidencia use los estilos
    tipo_incidencia = forms.ModelChoiceField(
        queryset=TipoIncidencia.objects.all(), # O .filter(activo=True) si tuvieras un campo 'activo'
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Encuesta
        # Campos del formulario basados en los requerimientos 
        fields = [
            'titulo_encuesta', 
            'descripcion', 
            'ubicacion', 
            'prioridad',
            'tipo_incidencia', 
            'nombre_vecino', 
            'celular_vecino', 
            'email_vecino', 
            'imagen', 
            'video', 
            'audio',
        ]
        
        # Añadimos clases de Bootstrap (SB Admin 2) a cada campo
        widgets = {
            'titulo_encuesta': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Luminaria rota en poste 12345'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describa el problema en detalle...'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Av. Principal con Calle Secundaria, frente al N° 150'}),
            'prioridad': forms.Select(attrs={'class': 'form-control'}),
            'nombre_vecino': forms.TextInput(attrs={'class': 'form-control'}),
            'celular_vecino': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+569...'}),
            'email_vecino': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'vecino@correo.com'}),
            
            # Widgets para subir archivos
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'video': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'audio': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }