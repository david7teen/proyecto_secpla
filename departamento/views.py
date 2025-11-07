from django.shortcuts import render
from .models import Usuario, Incidencia

def vista_departamento(request):
    usuario_activo = request.session.get('usuario_activo')
    departamento = Usuario.objects.get(id=usuario_activo['id'])

    incidencias = Incidencia.objects.filter(departamento_incidencia=departamento)

    resumen = {
        'pendientes': incidencias.filter(estado='Pendiente').count(),
        'derivadas': incidencias.filter(estado='Derivada').count(),
        'rechazadas': incidencias.filter(estado='Rechazada').count(),
        'finalizadas': incidencias.filter(estado='Finalizada').count(),
    }

    return render(request, 'Departamento/dashboard_departamento.html', {
        'usuario_activo': departamento,
        'resumen': resumen
    })

def incidencias_pendientes_departamento(request):
    usuario_activo = request.session.get('usuario_activo')
    departamento = Usuario.objects.get(id=usuario_activo['id'])
    pendientes = Incidencia.objects.filter(departamento_incidencia=departamento, estado='Pendiente')
    cuadrillas = Usuario.objects.filter(perfil='Cuadrilla')

    return render(request, 'Departamento/listado_incidencias_departamento.html', {
        'estado': estado,
        'incidencias': incidencias,
        'cuadrillas': cuadrillas,
        'usuario_activo': departamento
    })
