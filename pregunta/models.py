from django.db import models

class Pregunta(models.Model):
    nombre_pregunta = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre_pregunta
