from django.shortcuts import render, redirect, get_object_or_404
from SECPLA.models import Usuario
from incidencia.models import Incidencia
from django.contrib import messages

def vista_cuadrilla(request):
    """
    Muestra el Dashboard principal de la Cuadrilla.
    """
    usuario_activo_data = request.session.get('usuario_activo')
    if not usuario_activo_data or usuario_activo_data['perfil'] != 'Cuadrilla':
        return redirect('/login/secpla/') # Ajusta a tu URL de login
    
    cuadrilla = get_object_or_404(Usuario, id=usuario_activo_data['id'])

    # Incidencias asignadas a esta cuadrilla
    incidencias_asignadas = Incidencia.objects.filter(cuadrilla_asignada=cuadrilla)
    
    resumen = {
        'pendientes': incidencias_asignadas.filter(estado='Derivada').count(),
        'en_proceso': incidencias_asignadas.filter(estado='En proceso').count(),
        'finalizadas': incidencias_asignadas.filter(estado='Finalizada').count(),
        'rechazadas': incidencias_asignadas.filter(estado='Rechazada').count(),
    }

    # Mostramos las 5 pendientes más nuevas en el dashboard
    incidencias_pendientes = incidencias_asignadas.filter(estado='Derivada').order_by('-fecha_creacion')[:5]

    return render(request, 'cuadrilla/dashboard_cuadrilla.html', {
        'usuario_activo': cuadrilla,
        'resumen': resumen,
        'incidencias_pendientes': incidencias_pendientes
    })

def listar_incidencias_cuadrilla(request):
    """
    Este es el REQUISITO MÍNIMO:
    Muestra el listado de incidencias en el estado 'Derivada' (asignadas).
    """
    usuario_activo_data = request.session.get('usuario_activo')
    if not usuario_activo_data or usuario_activo_data['perfil'] != 'Cuadrilla':
        return redirect('/login/secpla/')
    
    cuadrilla = get_object_or_404(Usuario, id=usuario_activo_data['id'])
    
    # Filtramos solo las incidencias "Derivadas" (pendientes de tomar)
    incidencias_list = Incidencia.objects.filter(
        cuadrilla_asignada=cuadrilla,
        estado='Derivada' # Este es el estado en que las pueden ver
    ).order_by('fecha_creacion')
    
    return render(request, 'cuadrilla/listado_incidencias_cuadrilla.html', {
        'usuario_activo': cuadrilla,
        'incidencias': incidencias_list,
        'titulo_lista': 'Incidencias Pendientes (Asignadas)'
    })

def tomar_incidencia(request, incidencia_id):
    """
    Acción simple que cambia el estado a 'En proceso'.
    """
    incidencia = get_object_or_404(Incidencia, id=incidencia_id)
    # Aquí iría la lógica para asegurar que la incidencia pertenece a la cuadrilla
    incidencia.estado = 'En proceso'
    incidencia.save()
    messages.info(request, f'Incidencia #{incidencia.id} marcada como "En Proceso".')
    return redirect('dashboard_cuadrilla') # Redirige al dashboard

def rechazar_incidencia(request, incidencia_id):
    """
    REQUISITO MÍNIMO:
    Acción simple que cambia el estado a 'Rechazada'.
    """
    incidencia = get_object_or_404(Incidencia, id=incidencia_id)
    # Aquí iría la lógica para asegurar que la incidencia pertenece a la cuadrilla
    incidencia.estado = 'Rechazada'
    incidencia.save()
    messages.warning(request, f'Incidencia #{incidencia.id} ha sido rechazada.')
    return redirect('dashboard_cuadrilla') # Redirige al dashboard

def responder_incidencia(request, incidencia_id):
    """
    REQUISITO MÍNIMO:
    Muestra el formulario para "Finalizar" la incidencia.
    """
    incidencia = get_object_or_404(Incidencia, id=incidencia_id)

    if request.method == 'POST':
        # (Debes agregar estos campos a tu modelo Incidencia si no existen)
        # incidencia.descripcion_resolucion = request.POST.get('descripcion')
        # incidencia.evidencia_imagen = request.FILES.get('imagen')
        
        incidencia.estado = 'Finalizada'
        incidencia.save()
        
        messages.success(request, f'Incidencia #{incidencia.id} marcada como "Finalizada".')
        return redirect('dashboard_cuadrilla') # Redirige al dashboard

    return render(request, 'cuadrilla/responder_incidencia.html', {
        'incidencia': incidencia
    })

# --- VISTAS ADICIONALES (Listados secundarios) ---

def incidencias_en_proceso(request):
    """
    Listado de incidencias que la cuadrilla ya 'tomó'.
    """
    usuario_activo_data = request.session.get('usuario_activo')
    cuadrilla = get_object_or_404(Usuario, id=usuario_activo_data['id'])
    incidencias_list = Incidencia.objects.filter(
        cuadrilla_asignada=cuadrilla,
        estado='En proceso'
    ).order_by('fecha_creacion')
    
    return render(request, 'cuadrilla/listado_incidencias_cuadrilla.html', {
        'usuario_activo': cuadrilla,
        'incidencias': incidencias_list,
        'titulo_lista': 'Incidencias en Proceso'
    })

def incidencias_finalizadas(request):
    """
    Historial de incidencias finalizadas por la cuadrilla.
    """
    usuario_activo_data = request.session.get('usuario_activo')
    cuadrilla = get_object_or_404(Usuario, id=usuario_activo_data['id'])
    incidencias_list = Incidencia.objects.filter(
        cuadrilla_asignada=cuadrilla,
        estado='Finalizada'
    ).order_by('-fecha_finalizacion')
    
    return render(request, 'cuadrilla/listado_incidencias_cuadrilla.html', {
        'usuario_activo': cuadrilla,
        'incidencias': incidencias_list,
        'titulo_lista': 'Historial de Incidencias Finalizadas'
    })