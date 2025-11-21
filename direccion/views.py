from django.shortcuts import render, redirect, get_object_or_404
from SECPLA.models import Usuario
from incidencia.models import Incidencia
from direccion.models import Direccion
from departamento.models import Departamento
from django.contrib import messages
from django.utils import timezone

def vista_direccion(request):
    usuario_activo_data = request.session.get('usuario_activo')
    if not usuario_activo_data or usuario_activo_data['perfil'] != 'Dirección':
        return redirect('/login/secpla/')

    usuario_activo = get_object_or_404(Usuario, id=usuario_activo_data['id'])
    direccion = usuario_activo.direccion_asociada

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


def incidencias_pendientes(request):
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
        estado='Abierta'
    ).order_by('-fecha_creacion')
    
    cuadrillas = Usuario.objects.filter(
        perfil='Cuadrilla',
        estado='Activo',
        departamento_asociado__direccion_departamento=direccion
    )
    
    return render(request, 'direccion/listado_incidencias.html', {
        'usuario_activo': usuario_activo,
        'incidencias': incidencias_list,
        'estado_titulo': 'Abierta',
        'cuadrillas': cuadrillas
    })



def get_incidencias_por_estado(request, estado, template_name):
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


def derivar_incidencia_direccion(request, incidencia_id):
    if request.method != 'POST':
        return redirect('dir_incidencias_pendientes')

    usuario_activo_data = request.session.get('usuario_activo')
    if not usuario_activo_data or usuario_activo_data['perfil'] != 'Dirección':
        messages.error(request, 'No tienes permisos.')
        return redirect('/login/secpla/')
         
    usuario_activo = get_object_or_404(Usuario, id=usuario_activo_data['id'])
    incidencia = get_object_or_404(Incidencia, id=incidencia_id)
    
    if incidencia.direccion_incidencia != usuario_activo.direccion_asociada:
        messages.error(request, 'No tienes permiso para derivar esta incidencia.')
        return redirect('dir_incidencias_pendientes')
        
    cuadrilla_id = request.POST.get('cuadrilla_id')
    
    if not cuadrilla_id:
        messages.error(request, 'Debes seleccionar una cuadrilla.')
        return redirect('dir_incidencias_pendientes')

    try:
        cuadrilla_asignada = Usuario.objects.get(
            id=cuadrilla_id, 
            perfil='Cuadrilla', 
            departamento_asociado__direccion_departamento=usuario_activo.direccion_asociada
        )
        
        incidencia.cuadrilla_asignada = cuadrilla_asignada
        incidencia.estado = 'Derivada'
        incidencia.fecha_derivacion = timezone.now()
        incidencia.save()
        
        messages.success(request, f'Incidencia #{incidencia.id} derivada correctamente a {cuadrilla_asignada.nombre}.')
        
    except Usuario.DoesNotExist:
        messages.error(request, 'La cuadrilla seleccionada no es válida o no pertenece a tu dirección.')
    
    return redirect('dir_incidencias_pendientes')


def rechazar_incidencia_direccion(request, incidencia_id):
    usuario_activo_data = request.session.get('usuario_activo')
    if not usuario_activo_data or usuario_activo_data['perfil'] != 'Dirección':
        return redirect('/login/secpla/')

    usuario_activo = get_object_or_404(Usuario, id=usuario_activo_data['id'])
    incidencia = get_object_or_404(Incidencia, id=incidencia_id)
    
    if incidencia.direccion_incidencia != usuario_activo.direccion_asociada:
        messages.error(request, 'No tienes permiso para esta acción.')
        return redirect('dashboard_direccion')

    incidencia.estado = 'Rechazada'
    incidencia.save()
    messages.warning(request, f'Incidencia #{incidencia.id} ha sido rechazada.')
    return redirect('dir_incidencias_pendientes')


def editar_incidencia_direccion(request, incidencia_id):
    usuario_activo_data = request.session.get('usuario_activo')
    if not usuario_activo_data or usuario_activo_data['perfil'] != 'Dirección':
        return redirect('/login/secpla/')
        
    usuario_activo = get_object_or_404(Usuario, id=usuario_activo_data['id'])
    incidencia = get_object_or_404(Incidencia, id=incidencia_id)

    if incidencia.direccion_incidencia != usuario_activo.direccion_asociada:
        messages.error(request, 'No tienes permisos para editar esta incidencia.')
        return redirect('dashboard_direccion')
    
    if request.method == 'POST':
        try:
            incidencia.nombre_incidencia = request.POST.get('nombre_incidencia')
            incidencia.descripcion = request.POST.get('descripcion')
            incidencia.prioridad = request.POST.get('prioridad')
            incidencia.ubicacion = request.POST.get('ubicacion')
            incidencia.datos_vecino = request.POST.get('datos_vecino')

            direccion_id = request.POST.get('direccion_incidencia')
            departamento_id = request.POST.get('departamento_incidencia')
            
            if direccion_id:
                incidencia.direccion_incidencia = Direccion.objects.get(id=direccion_id)
            if departamento_id:
                incidencia.departamento_incidencia = Departamento.objects.get(id=departamento_id)

            if 'imagen' in request.FILES:
                incidencia.imagen = request.FILES['imagen']

            incidencia.save()
            messages.success(request, 'Incidencia actualizada correctamente.')
            return redirect('dashboard_direccion')

        except Exception as e:
            messages.error(request, f'Error al actualizar: {e}')
    
    direcciones = Direccion.objects.filter(estado='Activo')
    departamentos = Departamento.objects.filter(estado='Activo')

    return render(request, 'direccion/editar_incidencia.html', {
        'usuario_activo': usuario_activo,
        'inc': incidencia,
        'direcciones': direcciones,
        'departamentos': departamentos,
    })


def listar_todas_incidencias(request):
    usuario_activo_data = request.session.get('usuario_activo')
    if not usuario_activo_data or usuario_activo_data['perfil'] != 'Dirección':
        return redirect('/login/secpla/')
        
    usuario_activo = get_object_or_404(Usuario, id=usuario_activo_data['id'])
    direccion = usuario_activo.direccion_asociada

    if not direccion:
        messages.error(request, 'No tienes una dirección asociada.')
        return redirect('dashboard_direccion')

    incidencias_list = Incidencia.objects.filter(
        direccion_incidencia=direccion
    ).order_by('-fecha_creacion')
    
    cuadrillas = Usuario.objects.filter(
        perfil='Cuadrilla',
        estado='Activo',
        departamento_asociado__direccion_departamento=direccion
    )
    
    return render(request, 'direccion/listado_incidencias.html', {
        'usuario_activo': usuario_activo,
        'incidencias': incidencias_list,
        'estado_titulo': 'Todas',
        'cuadrillas': cuadrillas
    })

def listar_incidencias_direccion(request):
    usuario_activo_data = request.session.get('usuario_activo')
    if not usuario_activo_data or usuario_activo_data['perfil'] != 'Dirección':
        return redirect('/login/secpla/')
        
    usuario_activo = get_object_or_404(Usuario, id=usuario_activo_data['id'])
    direccion = usuario_activo.direccion_asociada

    if not direccion:
        messages.error(request, 'No tienes una dirección asociada.')
        return redirect('dashboard_direccion')

    incidencias_list = Incidencia.objects.filter(
        direccion_incidencia=direccion
    ).order_by('-fecha_creacion')
    
    estado_filtro = request.GET.get('estado')
    if estado_filtro:
        incidencias_list = incidencias_list.filter(estado=estado_filtro)
    
    estado_choices = Incidencia._meta.get_field('estado').choices
    cuadrillas = Usuario.objects.filter(
        perfil='Cuadrilla',
        estado='Activo',
        departamento_asociado__direccion_departamento=direccion
    )
    
    return render(request, 'direccion/listar_incidencias_direccion.html', {
        'usuario_activo': usuario_activo,
        'incidencias': incidencias_list,
        'estado_choices': estado_choices,
        'estado_filtro': estado_filtro,
        'cuadrillas': cuadrillas
    })
