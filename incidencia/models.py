from django.db import models
from SECPLA.models import Usuario
from direccion.models import Direccion
from departamento.models import Departamento

class Incidencia(models.Model):
    nombre_incidencia = models.CharField(max_length=100, blank=False, null=False)
    descripcion = models.CharField(max_length=200, blank=False, null=False, default='Sin descripción')

    direccion_incidencia = models.ForeignKey(Direccion, on_delete=models.CASCADE, null=False)
    departamento_incidencia = models.ForeignKey(Departamento, on_delete=models.CASCADE, null=False)

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

    territorial_creador = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='incidencias_territorial',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.nombre_incidencia