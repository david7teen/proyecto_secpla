from django.db import models
from encuesta.models import Encuesta
from incidencia.models import Incidencia
from SECPLA.models import Usuario

class Solicitud(models.Model):
    encuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE)
    creada_por = models.ForeignKey(Usuario, on_delete=models.CASCADE) 
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    ESTADO_CHOICES = [
        ('Derivada', 'Derivada'),
        ('En proceso', 'En proceso'),
        ('Finalizada', 'Finalizada'),
        ('Rechazada', 'Rechazada'),
        ('Cerrada', 'Cerrada'),
    ]
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Derivada')

    evidencia_imagen = models.ImageField(upload_to='solicitudes/evidencia/', blank=True, null=True)
    descripcion_resolucion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Solicitud #{self.id} - {self.encuesta.nombre_encuesta}"