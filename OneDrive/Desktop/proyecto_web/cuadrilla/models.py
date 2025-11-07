from django.db import models
from django.shortcuts import redirect

class Cuadrilla(models.Model):
    nombre_cuadrilla = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.nombre_cuadrilla