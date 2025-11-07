from django.shortcuts import render,redirect
from .models import Usuario, Incidencia

def vista_cuadrilla(request):
    usuario_activo = request.session.get('usuario_activo')
    cuadrilla = Usuario.objects.get(id=usuario_activo['id'])

    incidencias = Incidencia.objects.filter(cuadrilla_asignada=cuadrilla)

    resumen = {
        'pendientes': incidencias.filter(estado='Derivada').count(),
        'finalizadas': incidencias.filter(estado='Finalizada').count(),
    }

    return render(request, 'Cuadrilla/dashboard_cuadrilla.html', {
        'usuario_activo': cuadrilla,
        'resumen': resumen
    })

def incidencias_activas_cuadrilla(request):
    cuadrilla = Usuario.objects.get(id=request.session['usuario_activo']['id'])
    activas = Incidencia.objects.filter(cuadrilla_asignada=cuadrilla, estado='Derivada')
    return render(request, 'Cuadrilla/listado_incidencias_cuadrilla.html', {
        'incidencias': activas,
        'estado': 'En curso'
    })

def responder_incidencia(request, incidencia_id):
    incidencia = Incidencia.objects.get(id=incidencia_id)

    if request.method == 'POST':
        descripcion = request.POST.get('descripcion')
        imagen = request.FILES.get('imagen')

        incidencia.descripcion_respuesta = descripcion
        incidencia.imagen_respuesta = imagen
        incidencia.estado = 'Finalizada'
        incidencia.save()

        return redirect('/cuadrilla/incidencias/activas/')

    return render(request, 'Cuadrilla/responder_incidencia.html', {
        'incidencia': incidencia
    })