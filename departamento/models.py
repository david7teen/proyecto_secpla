from django.db import models
from django.shortcuts import redirect
from direccion.models import Direccion

class Departamento(models.Model):
    nombre_departamento = models.CharField(max_length=100)
    encargado_departamento = models.CharField(max_length=100)
    correo_encargado = models.EmailField()
    direccion_departamento = models.ForeignKey(Direccion, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, default='Activo')

    def __str__(self):
        return self.nombre_departamento
    

