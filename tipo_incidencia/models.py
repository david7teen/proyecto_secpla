from django.db import models
from direccion.models import Direccion
from departamento.models import Departamento
from SECPLA.models import Usuario  

class TipoIncidencia(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.CharField(max_length=200, default='Sin descripción')

    direccion = models.ForeignKey(Direccion, on_delete=models.CASCADE)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)

    creado_por = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tipos_incidencia_creados'
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Tipo de Incidencia"
        verbose_name_plural = "Tipos de Incidencia"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre