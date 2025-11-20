from django.shortcuts import render, redirect, get_object_or_404
from SECPLA.models import Usuario
from incidencia.models import Incidencia
from direccion.models import Direccion
from departamento.models import Departamento
from django.contrib import messages
from django.utils import timezone

def vista_departamento(request):
    usuario_activo_data = request.session.get('usuario_activo')
    if not usuario_activo_data or usuario_activo_data['perfil'] != 'Departamento':
        return redirect('/secpla/login/departamento/')
    
    usuario_activo = Usuario.objects.get(id=usuario_activo_data['id'])

    departamento_usuario = usuario_activo.departamento_asociado

    if not departamento_usuario:
        return render(request, 'departamento/dashboard_departamento.html', {
            'usuario_activo': usuario_activo,
            'departamento': None,
            'resumen': {},
            'incidencias': [],
            'error': 'Este usuario no tiene un departamento asociado.'
        })
    
    incidencias = Incidencia.objects.filter(departamento_incidencia=departamento_usuario)

    resumen = {
        'pendientes': incidencias.filter(estado='Abierta').count(),
        'derivadas': incidencias.filter(estado='Derivada').count(),
        'rechazadas': incidencias.filter(estado='Rechazada').count(),
        'finalizadas': incidencias.filter(estado='Finalizada').count(),
    }

    incidencias_recientes = incidencias.filter(estado='Abierta').order_by('-fecha_creacion')[:5]

    return render(request, 'departamento/dashboard_departamento.html', {
        'usuario_activo': usuario_activo,
        'departamento': departamento_usuario,
        'resumen': resumen,
        'incidencias': incidencias_recientes
    })

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
    if not usuario_activo_data or usuario_activo_data['perfil'] != 'Departamento':
        return redirect('/secpla/login/departamento/')
    
    usuario_activo = Usuario.objects.get(id=usuario_activo_data['id'])
    
    departamento_usuario = usuario_activo.departamento_asociado
    if not departamento_usuario:
        messages.error(request, 'No tienes un departamento asociado.')
        return redirect('vista_departamento')
    
    incidencias = Incidencia.objects.filter(
        departamento_incidencia=departamento_usuario,
        estado='Abierta'
    ).order_by('-id')
    
    cuadrillas = Usuario.objects.filter(
        perfil='Cuadrilla',
        estado='Activo',
        departamento_asociado=departamento_usuario 
    )
    
    return render(request, 'departamento/ver_pendientes.html', {
        'usuario_activo': usuario_activo,
        'departamento': departamento_usuario,
        'incidencias': incidencias,
        'cuadrillas': cuadrillas
    })

def ver_derivadas_departamento(request):
    usuario_activo_data = request.session.get('usuario_activo')
    if not usuario_activo_data or usuario_activo_data['perfil'] != 'Departamento':
        return redirect('/secpla/login/departamento/')
    
    usuario_activo = Usuario.objects.get(id=usuario_activo_data['id'])
    
    departamento_usuario = usuario_activo.departamento_asociado
    if not departamento_usuario:
        messages.error(request, 'No tienes un departamento asociado.')
        return redirect('vista_departamento')
    
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
    if not usuario_activo_data or usuario_activo_data['perfil'] != 'Departamento':
        return redirect('/secpla/login/departamento/')
    
    usuario_activo = Usuario.objects.get(id=usuario_activo_data['id'])
    
    departamento_usuario = usuario_activo.departamento_asociado
    if not departamento_usuario:
        messages.error(request, 'No tienes un departamento asociado.')
        return redirect('vista_departamento')
  
    
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
    if not usuario_activo_data or usuario_activo_data['perfil'] != 'Departamento':
        return redirect('/secpla/login/departamento/')
    
    usuario_activo = Usuario.objects.get(id=usuario_activo_data['id'])
    

    departamento_usuario = usuario_activo.departamento_asociado
    if not departamento_usuario:
        messages.error(request, 'No tienes un departamento asociado.')
        return redirect('vista_departamento')

    
    incidencias_finalizadas = Incidencia.objects.filter(
        departamento_incidencia=departamento_usuario,
        estado='Finalizada'
    ).order_by('-id')
    
    total_incidencias = Incidencia.objects.filter(
        departamento_incidencia=departamento_usuario
    ).count()
    
    porcentaje_eficiencia = 0
    if total_incidencias > 0:
        porcentaje_eficiencia = (incidencias_finalizadas.count() / total_incidencias) * 100
    
    return render(request, 'departamento/ver_finalizadas.html', {
        'usuario_activo': usuario_activo,
        'departamento': departamento_usuario,
        'incidencias': incidencias_finalizadas,
        'porcentaje_eficiencia': round(porcentaje_eficiencia, 1)
    })
    
    
def reporte_finalizadas(request):
    usuario_activo_data = request.session.get('usuario_activo')
    if not usuario_activo_data or usuario_activo_data['perfil'] != 'Departamento':
        return redirect('/secpla/login/departamento/')
    
    usuario_activo = Usuario.objects.get(id=usuario_activo_data['id'])
    

    departamento_usuario = usuario_activo.departamento_asociado
    if not departamento_usuario:
        messages.error(request, 'No tienes un departamento asociado.')
        return redirect('vista_departamento')

    
    incidencias = Incidencia.objects.filter(
        departamento_incidencia=departamento_usuario,
        estado='Finalizada'
    ).order_by('-id')
    
    return render(request, 'departamento/reporte_finalizadas.html', {
        'usuario_activo': usuario_activo,
        'departamento': departamento_usuario,
        'incidencias': incidencias
    })

def derivar_incidencia(request, incidencia_id):
    if request.method != 'POST':
        return redirect('ver_pendientes_departamento')

    usuario_activo_data = request.session.get('usuario_activo')
    if not usuario_activo_data:
        return redirect('/secpla/login/departamento/')
        
    usuario_activo = Usuario.objects.get(id=usuario_activo_data['id'])
    if usuario_activo.perfil != 'Departamento':
        messages.error(request, 'No tienes permisos de Departamento.')
        return redirect('/secpla/login/departamento/')
    
    incidencia = get_object_or_404(Incidencia, id=incidencia_id)
    
    if incidencia.departamento_incidencia != usuario_activo.departamento_asociado:
        messages.error(request, 'No tienes permiso para derivar esta incidencia.')
        return redirect('ver_pendientes_departamento')
        
    cuadrilla_id = request.POST.get('cuadrilla_id')
    
    if not cuadrilla_id:
        messages.error(request, 'Debes seleccionar una cuadrilla.')
        return redirect('ver_pendientes_departamento')

    try:
        cuadrilla_asignada = Usuario.objects.get(id=cuadrilla_id, perfil='Cuadrilla', departamento_asociado=usuario_activo.departamento_asociado)
        
        incidencia.cuadrilla_asignada = cuadrilla_asignada
        incidencia.estado = 'Derivada'
        incidencia.fecha_derivacion = timezone.now()
        incidencia.save()
        
        messages.success(request, f'Incidencia #{incidencia.id} derivada correctamente a {cuadrilla_asignada.nombre}.')
        
    except Usuario.DoesNotExist:
        messages.error(request, 'La cuadrilla seleccionada no es válida o no pertenece a tu departamento.')
    
    return redirect('ver_pendientes_departamento')


def rechazar_incidencia(request, incidencia_id):
    usuario_activo_data = request.session.get('usuario_activo')
    if not usuario_activo_data:
        return redirect('/secpla/login/departamento/')

    usuario_activo = Usuario.objects.get(id=usuario_activo_data['id'])
    if usuario_activo.perfil != 'Departamento':
        messages.error(request, 'No tienes permisos de Departamento.')
        return redirect('/secpla/login/departamento/')
    
    incidencia = get_object_or_404(Incidencia, id=incidencia_id)
    
    if incidencia.departamento_incidencia != usuario_activo.departamento_asociado:
        messages.error(request, 'No tienes permiso para esta acción.')
        return redirect('ver_pendientes_departamento')

    incidencia.estado = 'Rechazada'

    incidencia.save()
    
    messages.warning(request, f'Incidencia #{incidencia.id} ha sido rechazada.')
    
    return redirect('ver_pendientes_departamento')


def ver_incidencia_departamento(request, incidencia_id):
    usuario_activo_data = request.session.get('usuario_activo')
    if not usuario_activo_data or usuario_activo_data['perfil'] != 'Departamento':
        return redirect('/secpla/login/departamento/')
        
    usuario_activo = get_object_or_404(Usuario, id=usuario_activo_data['id'])
    incidencia = get_object_or_404(Incidencia, id=incidencia_id)

    if incidencia.departamento_incidencia != usuario_activo.departamento_asociado:
        messages.error(request, 'No tienes permisos para ver esta incidencia.')
        return redirect('ver_rechazadas_departamento')

    return render(request, 'departamento/ver_incidencia.html', {
        'usuario_activo': usuario_activo,
        'inc': incidencia
    })


def reabrir_incidencia(request, incidencia_id):

    usuario_activo_data = request.session.get('usuario_activo')
    if not usuario_activo_data or usuario_activo_data['perfil'] != 'Departamento':
        return redirect('/secpla/login/departamento/')
        
    usuario_activo = get_object_or_404(Usuario, id=usuario_activo_data['id'])
    incidencia = get_object_or_404(Incidencia, id=incidencia_id)

    if incidencia.departamento_incidencia != usuario_activo.departamento_asociado:
        messages.error(request, 'No tienes permisos para esta acción.')
        return redirect('ver_rechazadas_departamento')
    incidencia.estado = 'Abierta'
    incidencia.save()
    
    messages.success(request, f'Incidencia #{incidencia.id} ha sido re-abierta.')
    return redirect('ver_rechazadas_departamento')

from direccion.models import Direccion
from departamento.models import Departamento


def editar_incidencia_departamento(request, incidencia_id):

    usuario_activo_data = request.session.get('usuario_activo')
    if not usuario_activo_data or usuario_activo_data['perfil'] != 'Departamento':
        return redirect('/secpla/login/departamento/')
        
    usuario_activo = get_object_or_404(Usuario, id=usuario_activo_data['id'])
    incidencia = get_object_or_404(Incidencia, id=incidencia_id)

    if incidencia.departamento_incidencia != usuario_activo.departamento_asociado:
        messages.error(request, 'No tienes permisos para editar esta incidencia.')
        return redirect('ver_rechazadas_departamento')
    
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
            incidencia.estado = 'Abierta' 

            incidencia.save()
            messages.success(request, 'Incidencia actualizada y marcada como "Abierta".')
            return redirect('ver_pendientes_departamento')

        except (Direccion.DoesNotExist, Departamento.DoesNotExist):
            messages.error(request, 'La dirección o departamento seleccionado no es válido.')
        except Exception as e:
            messages.error(request, f'Ocurrió un error: {e}')
    
    direcciones = Direccion.objects.filter(estado='Activo')
    departamentos = Departamento.objects.filter(estado='Activo')

    return render(request, 'departamento/editar_incidencia.html', {
        'usuario_activo': usuario_activo,
        'inc': incidencia,
        'direcciones': direcciones,
        'departamentos': departamentos,
    })
