from django.db import models

class Territorial(models.Model):
    nombre_territorial = models.CharField(max_length=100)
    apellido_territorial = models.CharField(max_length=100)
    correo_territorial = models.EmailField()
    telefono_territorial = models.CharField(max_length=100)
    estado = models.CharField(max_length=20, default='Activo')

    def __str__(self):
        return self.nombre_territorial