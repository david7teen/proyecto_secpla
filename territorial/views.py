from django.shortcuts import render, redirect
from .models import Usuario, Incidencia
from encuesta.forms import IncidenciaForm

def vista_territorial(request):
    usuario_activo = Usuario.objects.get(id=request.session['usuario_activo']['id'])

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

def crear_incidencia(request):
    usuario_activo = Usuario.objects.get(id=request.session['usuario_activo']['id'])
    if request.method == 'POST':
        form = IncidenciaForm(request.POST, request.FILES)
        if form.is_valid():
            incidencia = form.save(commit=False)
            incidencia.territorial_creador = usuario_activo 
            incidencia.estado = 'Abierta'
            incidencia.save()
            return redirect('/territorial/dashboard/') 
    else:
        form = IncidenciaForm()
    context = {
        'form': form,
        'usuario_activo': usuario_activo
    }
    return render(request, 'territorial/crear_incidencia.html', context)