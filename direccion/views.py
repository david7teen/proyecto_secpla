from django.shortcuts import render, redirect, get_object_or_404
from SECPLA.models import Usuario
from incidencia.models import Incidencia
from direccion.models import Direccion
from django.contrib import messages

def vista_direccion(request):
    usuario_activo_data = request.session.get('usuario_activo')
    if not usuario_activo_data or usuario_activo_data['perfil'] != 'Dirección':
        return redirect('/login/secpla/') # Ajusta a tu URL de login

    usuario_activo = get_object_or_404(Usuario, id=usuario_activo_data['id'])
    direccion = usuario_activo.direccion_asociada # (Campo del Prerrequisito)

    if not direccion:
        return render(request, 'direccion/dashboard_direccion.html', {
            'usuario_activo': usuario_activo,
            'resumen': {},
            'incidencias': [],
            'error': 'Este usuario no tiene una dirección asociada.'
        })

    incidencias = Incidencia.objects.filter(direccion_incidencia=direccion)
    resumen = {
        'abiertas': incidencias.filter(estado='Abierta').count(),
        'derivadas': incidencias.filter(estado='Derivada').count(),
        'rechazadas': incidencias.filter(estado='Rechazada').count(),
        'finalizadas': incidencias.filter(estado='Finalizada').count(),
    }
    
    incidencias_recientes = incidencias.order_by('-fecha_creacion')[:5]

    return render(request, 'direccion/dashboard_direccion.html', {
        'usuario_activo': usuario_activo,
        'direccion': direccion,
        'incidencias': incidencias_recientes,
        'resumen': resumen
    })

def get_incidencias_por_estado(request, estado, template_name):
    """Función auxiliar para evitar repetir código en los listados"""
    usuario_activo_data = request.session.get('usuario_activo')
    if not usuario_activo_data or usuario_activo_data['perfil'] != 'Dirección':
        return redirect('/login/secpla/')
        
    usuario_activo = get_object_or_404(Usuario, id=usuario_activo_data['id'])
    direccion = usuario_activo.direccion_asociada

    if not direccion:
        messages.error(request, 'No tienes una dirección asociada.')
        return redirect('dashboard_direccion')

    incidencias_list = Incidencia.objects.filter(
        direccion_incidencia=direccion,
        estado=estado
    ).order_by('-fecha_creacion')
    
    return render(request, template_name, {
        'usuario_activo': usuario_activo,
        'incidencias': incidencias_list,
        'estado_titulo': estado
    })

def incidencias_pendientes(request):
    return get_incidencias_por_estado(request, 'Abierta', 'direccion/listado_incidencias.html')

def incidencias_derivadas(request):
    return get_incidencias_por_estado(request, 'Derivada', 'direccion/listado_incidencias.html')

def incidencias_rechazadas(request):
    return get_incidencias_por_estado(request, 'Rechazada', 'direccion/listado_incidencias.html')

def incidencias_finalizadas(request):
    return get_incidencias_por_estado(request, 'Finalizada', 'direccion/listado_incidencias.html')

def ver_incidencia_direccion(request, incidencia_id):
    usuario_activo_data = request.session.get('usuario_activo')
    if not usuario_activo_data or usuario_activo_data['perfil'] != 'Dirección':
        return redirect('/login/secpla/')
        
    usuario_activo = get_object_or_404(Usuario, id=usuario_activo_data['id'])
    incidencia = get_object_or_404(Incidencia, id=incidencia_id)
    if incidencia.direccion_incidencia != usuario_activo.direccion_asociada:
        messages.error(request, 'No tienes permisos para ver esta incidencia.')
        return redirect('dashboard_direccion')

    return render(request, 'direccion/ver_incidencia.html', {
        'usuario_activo': usuario_activo,
        'inc': incidencia
    })