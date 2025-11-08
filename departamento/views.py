from django.shortcuts import render, redirect, get_object_or_404
from SECPLA.models import Usuario
from incidencia.models import Incidencia
from departamento.models import Departamento

def vista_departamento(request):
    usuario_activo_data = request.session.get('usuario_activo')
    if not usuario_activo_data:
        return redirect('/secpla/login/departamento/')
    
    usuario_activo = Usuario.objects.get(id=usuario_activo_data['id'])

    # Obtener el departamento del usuario
    try:
        departamento_usuario = Departamento.objects.get(encargado_departamento=usuario_activo.nombre + " " + usuario_activo.apellido)
    except Departamento.DoesNotExist:
        # Si no encuentra por nombre, usar el primero disponible (temporal)
        departamento_usuario = Departamento.objects.first()

    # Filtrar incidencias del departamento
    incidencias = Incidencia.objects.filter(departamento_incidencia=departamento_usuario)

    resumen = {
        'pendientes': incidencias.filter(estado='Abierta').count(),
        'derivadas': incidencias.filter(estado='Derivada').count(),
        'rechazadas': incidencias.filter(estado='Rechazada').count(),
        'finalizadas': incidencias.filter(estado='Finalizada').count(),
    }

    return render(request, 'departamento/dashboard_departamento.html', {
        'usuario_activo': usuario_activo,
        'departamento': departamento_usuario,
        'resumen': resumen
    })

def ver_pendientes_departamento(request):
    usuario_activo_data = request.session.get('usuario_activo')
    if not usuario_activo_data:
        return redirect('/secpla/login/departamento/')
    
    usuario_activo = Usuario.objects.get(id=usuario_activo_data['id'])
    
    # Obtener departamento del usuario
    try:
        departamento_usuario = Departamento.objects.get(encargado_departamento=usuario_activo.nombre + " " + usuario_activo.apellido)
    except Departamento.DoesNotExist:
        departamento_usuario = Departamento.objects.first()
    
    # Filtrar incidencias del departamento con estado Abierta (Pendiente)
    incidencias = Incidencia.objects.filter(
        departamento_incidencia=departamento_usuario,
        estado='Abierta'
    ).order_by('-id')
    
    return render(request, 'departamento/ver_pendientes.html', {
        'usuario_activo': usuario_activo,
        'departamento': departamento_usuario,
        'incidencias': incidencias
    })

def ver_derivadas_departamento(request):
    usuario_activo_data = request.session.get('usuario_activo')
    if not usuario_activo_data:
        return redirect('/secpla/login/departamento/')
    
    usuario_activo = Usuario.objects.get(id=usuario_activo_data['id'])
    
    try:
        departamento_usuario = Departamento.objects.get(encargado_departamento=usuario_activo.nombre + " " + usuario_activo.apellido)
    except Departamento.DoesNotExist:
        departamento_usuario = Departamento.objects.first()
    
    incidencias = Incidencia.objects.filter(
        departamento_incidencia=departamento_usuario,
        estado='Derivada'
    ).order_by('-id')
    
    return render(request, 'departamento/ver_derivadas.html', {
        'usuario_activo': usuario_activo,
        'departamento': departamento_usuario,
        'incidencias': incidencias
    })

def ver_rechazadas_departamento(request):
    usuario_activo_data = request.session.get('usuario_activo')
    if not usuario_activo_data:
        return redirect('/secpla/login/departamento/')
    
    usuario_activo = Usuario.objects.get(id=usuario_activo_data['id'])
    
    try:
        departamento_usuario = Departamento.objects.get(encargado_departamento=usuario_activo.nombre + " " + usuario_activo.apellido)
    except Departamento.DoesNotExist:
        departamento_usuario = Departamento.objects.first()
    
    incidencias = Incidencia.objects.filter(
        departamento_incidencia=departamento_usuario,
        estado='Rechazada'
    ).order_by('-id')
    
    return render(request, 'departamento/ver_rechazadas.html', {
        'usuario_activo': usuario_activo,
        'departamento': departamento_usuario,
        'incidencias': incidencias
    })

def ver_finalizadas_departamento(request):
    usuario_activo_data = request.session.get('usuario_activo')
    if not usuario_activo_data:
        return redirect('/secpla/login/departamento/')
    
    usuario_activo = Usuario.objects.get(id=usuario_activo_data['id'])
    
    try:
        departamento_usuario = Departamento.objects.get(encargado_departamento=usuario_activo.nombre + " " + usuario_activo.apellido)
    except Departamento.DoesNotExist:
        departamento_usuario = Departamento.objects.first()
    
    incidencias = Incidencia.objects.filter(
        departamento_incidencia=departamento_usuario,
        estado='Finalizada'
    ).order_by('-id')
    
    # Calcular porcentaje de eficiencia
    total_incidencias = Incidencia.objects.filter(
        departamento_incidencia=departamento_usuario
    ).count()
    
    porcentaje_eficiencia = 0
    if total_incidencias > 0:
        porcentaje_eficiencia = (incidencias.count() / total_incidencias) * 100
    
    return render(request, 'departamento/ver_finalizadas.html', {
        'usuario_activo': usuario_activo,
        'departamento': departamento_usuario,
        'incidencias': incidencias,
        'porcentaje_eficiencia': round(porcentaje_eficiencia, 1)
    })
    
    
def reporte_finalizadas(request):
    usuario_activo_data = request.session.get('usuario_activo')
    if not usuario_activo_data:
        return redirect('/secpla/login/departamento/')
    
    usuario_activo = Usuario.objects.get(id=usuario_activo_data['id'])
    
    try:
        departamento_usuario = Departamento.objects.get(encargado_departamento=usuario_activo.nombre + " " + usuario_activo.apellido)
    except Departamento.DoesNotExist:
        departamento_usuario = Departamento.objects.first()
    
    incidencias = Incidencia.objects.filter(
        departamento_incidencia=departamento_usuario,
        estado='Finalizada'
    ).order_by('-id')
    
    return render(request, 'departamento/reporte_finalizadas.html', {
        'usuario_activo': usuario_activo,
        'departamento': departamento_usuario,
        'incidencias': incidencias
    })
