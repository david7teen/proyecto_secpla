from django.db import models
from tipo_incidencia.models import TipoIncidencia 
from pregunta.models import Pregunta

class Encuesta(models.Model):
    nombre_encuesta = models.CharField(max_length=100)
    descripcion_incidente = models.TextField()
    ubicacion = models.CharField(max_length=200)
    imagen = models.ImageField(upload_to='encuestas/imagenes/', blank=True, null=True)
    video = models.FileField(upload_to='encuestas/videos/', blank=True, null=True)
    audio = models.FileField(upload_to='encuestas/audios/', blank=True, null=True)

    preguntas = models.ManyToManyField(Pregunta)  

    PRIORIDAD_CHOICES = [
        ('Alta', 'Alta'),
        ('Normal', 'Normal'),
        ('Baja', 'Baja'),
    ]
    prioridad = models.CharField(max_length=10, choices=PRIORIDAD_CHOICES)

    datos_vecino = models.TextField(blank=True, null=True)
    tipo_incidencia = models.ForeignKey(TipoIncidencia, on_delete=models.CASCADE, null=True)

    estado = models.CharField(max_length=20, choices=[
    ('Abierta', 'Abierta'),
    ('Derivada', 'Derivada'),
    ('En Proceso', 'En Proceso'),
    ('Finalizada', 'Finalizada'),
    ('Cerrada', 'Cerrada'),
    ('Rechazada', 'Rechazada'),
    ], default='Abierta')
  

    CATEGORIA_CHOICES = [
        ('Creada', 'Creada'),
        ('Vigente', 'Vigente'),
        ('Bloqueada', 'Bloqueada'),
    ]
    categoria = models.CharField(
        max_length=20,
        choices=CATEGORIA_CHOICES,
        default='Creada'
    )

    def __str__(self):
        return self.nombre_encuesta