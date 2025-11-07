from django.shortcuts import render
from .models import Usuario, Incidencia

def vista_territorial(request):
    usuario_activo = Usuario.objects.get(id=request.session['usuario_activo']['id'])

    # Filtrar incidencias creadas por este territorial
    incidencias = Incidencia.objects.filter(territorial_creador=usuario_activo)

    resumen = {
        'abiertas': incidencias.filter(estado='Abierta').count(),
        'derivadas': incidencias.filter(estado='Derivada').count(),
        'rechazadas': incidencias.filter(estado='Rechazada').count(),
        'proceso': incidencias.filter(estado='Proceso').count(),
        'finalizadas': incidencias.filter(estado='Finalizada').count(),
        'cerradas': incidencias.filter(estado='Cerrada').count(),
        'total': incidencias.count()
    }

    return render(request, 'Territorial/dashboard_territorial.html', {
        'usuario_activo': usuario_activo,
        'resumen': resumen
    })