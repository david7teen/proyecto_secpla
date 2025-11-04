from django import forms
# Importamos los modelos necesarios
from .models import Direccion, Departamento, Cuadrilla

# ... (Aquí iría tu DireccionForm y DepartamentoForm existentes) ...

# ---------- FORMULARIO DINÁMICO DE CUADRILLA (NUEVO) ----------
class CuadrillaForm(forms.ModelForm):
    class Meta:
        model = Cuadrilla
        # Omitimos 'estado' para que se maneje por las vistas (bloquear/activar)
        # igual que haces con DepartamentoForm
        fields = ['nombre', 'departamento', 'usuario']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre de la cuadrilla'
            }),
            'departamento': forms.Select(attrs={'class': 'form-select'}),
            # Como 'usuario' es IntegerField, usamos NumberInput.
            # Si fuera un ForeignKey a Usuario, usaríamos forms.Select.
            'usuario': forms.NumberInput(attrs={ 
                'class': 'form-control',
                'placeholder': 'ID de Usuario (Opcional)'
            }),
        }

    # Comportamiento dinámico:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Solo mostrar departamentos activos, siguiendo el patrón de DepartamentoForm
        self.fields['departamento'].queryset = Departamento.objects.filter(estado='Activo')