from django.db import models
from SECPLA.models import Usuario
from direccion.models import Direccion
from departamento.models import Departamento
from tipo_incidencia.models import TipoIncidencia
from django.utils import timezone

class Incidencia(models.Model):
    nombre_incidencia = models.CharField(max_length=100, blank=False, null=False)
    descripcion = models.TextField(blank=False, null=False, default='Sin descripción')

    direccion_incidencia = models.ForeignKey(Direccion, on_delete=models.CASCADE, null=False)
    departamento_incidencia = models.ForeignKey(Departamento, on_delete=models.CASCADE, null=False)
    tipo_incidencia = models.ForeignKey(TipoIncidencia, on_delete=models.CASCADE, null=True, blank=True)

    cuadrilla_asignada = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='incidencias_asignadas'
    )
    
    territorial_creador = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='incidencias_territorial',
        null=True,
        blank=True
    )

    PRIORIDAD_CHOICES = [
        ('Alta', 'Alta'),
        ('Normal', 'Normal'),
        ('Baja', 'Baja'),
    ]
    prioridad = models.CharField(max_length=10, choices=PRIORIDAD_CHOICES, default='Normal')

    estado = models.CharField(
        max_length=20,
        choices=[
            ('Abierta', 'Abierta'),
            ('Derivada', 'Derivada'),
            ('Rechazada', 'Rechazada'),
            ('En proceso', 'En proceso'),
            ('Finalizada', 'Finalizada'),
            ('Cerrada', 'Cerrada'),
        ],
        default='Abierta'
    )

    ubicacion = models.CharField(max_length=200, blank=True, null=True)
    imagen = models.ImageField(upload_to='incidencias/imagenes/', blank=True, null=True)
    datos_vecino = models.TextField(blank=True, null=True)

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_derivacion = models.DateTimeField(blank=True, null=True)
    fecha_finalizacion = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.nombre_incidencia

    def save(self, *args, **kwargs):
        if self.estado == 'Derivada' and not self.fecha_derivacion:
            self.fecha_derivacion = timezone.now()
        if self.estado == 'Finalizada' and not self.fecha_finalizacion:
            self.fecha_finalizacion = timezone.now()
        super().save(*args, **kwargs)
