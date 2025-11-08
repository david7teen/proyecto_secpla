from django.shortcuts import render, redirect
from .models import Usuario, Incidencia, Direccion
from django.shortcuts import get_object_or_404

def vista_direccion(request):
    usuario_activo_data = request.session.get('usuario_activo')
    if not usuario_activo_data:
        return redirect('/secpla/login/direccion/')

    usuario = Usuario.objects.filter(id=usuario_activo_data['id'], perfil='Dirección').first()
    if not usuario or not usuario.direccion_asociada:
        return render(request, 'Direccion/dashboard_direccion.html', {
            'usuario_activo': usuario,
            'incidencias': [],
            'resumen': {},
            'advertencia': 'Este perfil no tiene una dirección asociada.'
        })

    direccion = usuario.direccion_asociada
    incidencias = Incidencia.objects.filter(direccion_incidencia=direccion)

    resumen = {
        'abiertas': incidencias.filter(estado='Abierta').count(),
        'pendientes': incidencias.filter(estado='Pendiente').count(),
        'derivadas': incidencias.filter(estado='Derivada').count(),
        'rechazadas': incidencias.filter(estado='Rechazada').count(),
        'finalizadas': incidencias.filter(estado='Finalizada').count(),
    }

    return render(request, 'Direccion/dashboard_direccion.html', {
        'usuario_activo': usuario,
        'direccion': direccion,
        'incidencias': incidencias,
        'resumen': resumen
    })

def incidencias_pendientes(request):
    usuario_activo = request.session.get('usuario_activo')
    direccion = Usuario.objects.get(id=usuario_activo['id'])
    pendientes = Incidencia.objects.filter(direccion_incidencia=direccion, estado='Pendiente')
    return render(request, 'Direccion/listado_incidencias.html', {
        'estado': 'Pendientes',
        'incidencias': pendientes
    })



