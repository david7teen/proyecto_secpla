from django.shortcuts import render,redirect, get_object_or_404
from SECPLA.models import Usuario
from incidencia.models import Incidencia

def vista_cuadrilla(request):
    usuario_activo_data = request.session.get('usuario_activo')
    if not usuario_activo_data:
        return redirect('/secpla/login/cuadrilla/')
    
    cuadrilla = Usuario.objects.get(id=usuario_activo_data['id'])

    # Incidencias asignadas a esta cuadrilla
    incidencias_asignadas = Incidencia.objects.filter(cuadrilla_asignada=cuadrilla)
    
    resumen = {
        'pendientes': incidencias_asignadas.filter(estado='Derivada').count(),
        'en_proceso': incidencias_asignadas.filter(estado='En proceso').count(),
        'finalizadas': incidencias_asignadas.filter(estado='Finalizada').count(),
        'rechazadas': incidencias_asignadas.filter(estado='Rechazada').count(),
        'total': incidencias_asignadas.count()
    }

    # Incidencias pendientes (para trabajar ahora)
    incidencias_pendientes = incidencias_asignadas.filter(estado='Derivada')[:5]

    return render(request, 'Cuadrilla/dashboard_cuadrilla.html', {
        'usuario_activo': cuadrilla,
        'resumen': resumen,
        'incidencias_pendientes': incidencias_pendientes
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


def listado_incidencias_cuadrilla(request):
    usuario_activo_data = request.session.get('usuario_activo')
    if not usuario_activo_data:
        return redirect('/secpla/login/cuadrilla/')
    
    cuadrilla = Usuario.objects.get(id=usuario_activo_data['id'])
    incidencias = Incidencia.objects.filter(cuadrilla_asignada=cuadrilla)
    
    return render(request, 'Cuadrilla/listado_incidencias_cuadrilla.html', {
        'usuario_activo': cuadrilla,
        'incidencias': incidencias
    })

def tomar_incidencia(request, incidencia_id):
    incidencia = get_object_or_404(Incidencia, id=incidencia_id)
    incidencia.estado = 'En proceso'
    incidencia.save()
    return redirect('dashboard_cuadrilla')

def rechazar_incidencia(request, incidencia_id):
    incidencia = get_object_or_404(Incidencia, id=incidencia_id)
    incidencia.estado = 'Rechazada'
    incidencia.save()
    return redirect('dashboard_cuadrilla')

def incidencias_proceso(request):
    usuario_activo_data = request.session.get('usuario_activo')
    if not usuario_activo_data:
        return redirect('/secpla/login/cuadrilla/')
    
    cuadrilla = Usuario.objects.get(id=usuario_activo_data['id'])
    incidencias = Incidencia.objects.filter(cuadrilla_asignada=cuadrilla, estado='En proceso')
    
    return render(request, 'Cuadrilla/incidencias_proceso.html', {
        'usuario_activo': cuadrilla,
        'incidencias': incidencias
    })

def incidencias_finalizadas_cuadrilla(request):
    usuario_activo_data = request.session.get('usuario_activo')
    if not usuario_activo_data:
        return redirect('/secpla/login/cuadrilla/')
    
    cuadrilla = Usuario.objects.get(id=usuario_activo_data['id'])
    incidencias = Incidencia.objects.filter(cuadrilla_asignada=cuadrilla, estado='Finalizada')
    
    return render(request, 'Cuadrilla/incidencias_finalizadas.html', {
        'usuario_activo': cuadrilla,
        'incidencias': incidencias
    })

def reporte_trabajo(request):
    usuario_activo_data = request.session.get('usuario_activo')
    if not usuario_activo_data:
        return redirect('/secpla/login/cuadrilla/')
    
    cuadrilla = Usuario.objects.get(id=usuario_activo_data['id'])
    incidencias = Incidencia.objects.filter(cuadrilla_asignada=cuadrilla)
    
    return render(request, 'Cuadrilla/reporte_trabajo.html', {
        'usuario_activo': cuadrilla,
        'incidencias': incidencias
    })
    
    
def listado_incidencias_cuadrilla(request):
    usuario_activo_data = request.session.get('usuario_activo')
    if not usuario_activo_data:
        return redirect('/secpla/login/cuadrilla/')
    
    cuadrilla = Usuario.objects.get(id=usuario_activo_data['id'])
    incidencias = Incidencia.objects.filter(cuadrilla_asignada=cuadrilla)
    
    return render(request, 'Cuadrilla/listado_incidencias_cuadrilla.html', {
        'usuario_activo': cuadrilla,
        'incidencias': incidencias
    })

def tomar_incidencia(request, incidencia_id):
    incidencia = Incidencia.objects.get(id=incidencia_id)
    incidencia.estado = 'En proceso'
    incidencia.save()
    return redirect('/cuadrilla/')

def rechazar_incidencia(request, incidencia_id):
    incidencia = Incidencia.objects.get(id=incidencia_id)
    incidencia.estado = 'Rechazada'
    incidencia.save()
    return redirect('/cuadrilla/')

def incidencias_proceso(request):
    usuario_activo_data = request.session.get('usuario_activo')
    if not usuario_activo_data:
        return redirect('/secpla/login/cuadrilla/')
    
    cuadrilla = Usuario.objects.get(id=usuario_activo_data['id'])
    incidencias = Incidencia.objects.filter(cuadrilla_asignada=cuadrilla, estado='En proceso')
    
    return render(request, 'Cuadrilla/incidencias_proceso.html', {
        'usuario_activo': cuadrilla,
        'incidencias': incidencias
    })

def incidencias_finalizadas_cuadrilla(request):
    usuario_activo_data = request.session.get('usuario_activo')
    if not usuario_activo_data:
        return redirect('/secpla/login/cuadrilla/')
    
    cuadrilla = Usuario.objects.get(id=usuario_activo_data['id'])
    incidencias = Incidencia.objects.filter(cuadrilla_asignada=cuadrilla, estado='Finalizada')
    
    return render(request, 'Cuadrilla/incidencias_finalizadas.html', {
        'usuario_activo': cuadrilla,
        'incidencias': incidencias
    })

def reporte_trabajo(request):
    usuario_activo_data = request.session.get('usuario_activo')
    if not usuario_activo_data:
        return redirect('/secpla/login/cuadrilla/')
    
    cuadrilla = Usuario.objects.get(id=usuario_activo_data['id'])
    incidencias = Incidencia.objects.filter(cuadrilla_asignada=cuadrilla)
    
    return render(request, 'Cuadrilla/reporte_trabajo.html', {
        'usuario_activo': cuadrilla,
        'incidencias': incidencias
    })
