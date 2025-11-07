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
    


def derivar_incidencia(request, incidencia_id):
    if request.method == 'POST':
        cuadrilla_id = request.POST.get('cuadrilla_id')
        incidencia = Incidencia.objects.get(id=incidencia_id)
        cuadrilla = Usuario.objects.get(id=cuadrilla_id)

        incidencia.cuadrilla_asignada = cuadrilla
        incidencia.estado = 'Derivada'
        incidencia.save()

    return redirect('/departamento/incidencias/pendientes/')