from django.db import models

class Direccion(models.Model):
    nombre_direccion = models.CharField(max_length=100)
    nombre_encargado = models.CharField(max_length=100)
    correo_encargado = models.EmailField()
    estado = models.CharField(max_length=20, default='Activo')

    def __str__(self):
        return self.nombre_direccion
