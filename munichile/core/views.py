from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from registration.models import Profile
from gestion.models import Solicitud
from gestion.models import Direccion, Departamento, Solicitud, UsuarioCuadrilla
from django.db.models import Q
from django.utils import timezone


def home(request):
    return redirect('login')

@login_required
def check_profile(request):
    try:
        profile = request.user.profile
        print(f"DEBUG: Usuario {request.user.username}, Perfil: {profile.perfil}")
        
        if profile.perfil == 'admin':
            return redirect('dashboard_secpla')
        elif profile.perfil == 'direccion':
            return redirect('dashboard_direccion')
        elif profile.perfil == 'departamento':
            return redirect('dashboard_departamento')
        elif profile.perfil == 'cuadrilla':
            return redirect('dashboard_cuadrilla')
        elif profile.perfil == 'territorial':
            return redirect('dashboard_territorial')
        else:
            messages.error(request, 'Perfil no reconocido')
            return redirect('logout')
            
    except Profile.DoesNotExist:
        messages.error(request, 'Perfil no configurado')
        return redirect('logout')

@login_required
def dashboard_secpla(request):
    if request.user.profile.perfil != 'admin':
        messages.error(request, 'Acceso denegado')
        return redirect('check_profile')
    
    # Métricas
    total_usuarios = User.objects.count()
    total_incidencias = Solicitud.objects.count()
    incidencias_derivadas = Solicitud.objects.filter(estado='derivada').count()
    incidencias_rechazadas = Solicitud.objects.filter(estado='rechazada').count()
    incidencias_finalizadas = Solicitud.objects.filter(estado='finalizada').count()
    incidencias_en_proceso = Solicitud.objects.filter(estado='en_proceso').count()
    
    # Distribución por estado
    from django.db.models import Count
    distribucion_estados = Solicitud.objects.values('estado').annotate(total=Count('id'))
    
    # Últimas solicitudes
    ultimas_solicitudes = Solicitud.objects.select_related('encuesta', 'territorial').order_by('-created')[:10]
    
    metrics = {
        'total_usuarios': total_usuarios,
        'total_incidencias': total_incidencias,
        'incidencias_derivadas': incidencias_derivadas,
        'incidencias_rechazadas': incidencias_rechazadas,
        'incidencias_finalizadas': incidencias_finalizadas,
        'incidencias_en_proceso': incidencias_en_proceso,
    }
    
    context = {
        'metrics': metrics,
        'distribucion_estados': distribucion_estados,
        'ultimas_solicitudes': ultimas_solicitudes,
        'perfil': 'SECPLA'
    }
    return render(request, 'core/dashboard_secpla.html', context)

@login_required
def dashboard_territorial(request):
    if request.user.profile.perfil != 'territorial':
        messages.error(request, 'Acceso denegado')
        return redirect('check_profile')
    
    solicitudes = Solicitud.objects.filter(territorial=request.user)
    
    # AGREGAR: tipos de incidencia disponibles
    from gestion.models import TipoIncidencia
    tipos_incidencia = TipoIncidencia.objects.filter(state='Activo')[:10]
    
    # AGREGAR: solicitudes por tipo
    from django.db.models import Count
    solicitudes_por_tipo = solicitudes.values(
        'encuesta__tipo_incidencia__nombre'
    ).annotate(total=Count('id'))
    
    metrics = {
        'total_creadas': solicitudes.count(),
        'abiertas': solicitudes.filter(estado='creada').count(),
        'derivadas': solicitudes.filter(estado='derivada').count(),
        'rechazadas': solicitudes.filter(estado='rechazada').count(),
        'finalizadas': solicitudes.filter(estado='finalizada').count(),
    }
    
    context = {
        'metrics': metrics,
        'solicitudes': solicitudes.order_by('-created')[:10],
        'tipos_incidencia': tipos_incidencia,
        'solicitudes_por_tipo': solicitudes_por_tipo,
        'perfil': 'Territorial'
    }
    return render(request, 'core/dashboard_territorial.html', context)

@login_required
def dashboard_direccion(request):
    if request.user.profile.perfil != 'direccion':
        messages.error(request, 'Acceso denegado')
        return redirect('check_profile')
    
    try:
        # Obtener direcciones del usuario actual
        direcciones_usuario = Direccion.objects.filter(
            Q(nombre_encargado=request.user.get_full_name()) | 
            Q(correo_encargado=request.user.email)
        )
        
        # Obtener solicitudes de los departamentos de estas direcciones
        departamentos_ids = Departamento.objects.filter(
            direccion__in=direcciones_usuario
        ).values_list('id', flat=True)
        
        solicitudes = Solicitud.objects.filter(
            departamento_asignado_id__in=departamentos_ids
        )
        
        # AGREGAR: Calcular solicitudes por departamento
        solicitudes_por_departamento = []
        for departamento in Departamento.objects.filter(direccion__in=direcciones_usuario):
            depto_solicitudes = solicitudes.filter(departamento_asignado=departamento)
            solicitudes_por_departamento.append({
                'nombre_departamento': departamento.nombre_departamento,
                'total': depto_solicitudes.count(),
                'pendientes': depto_solicitudes.filter(estado='derivada').count(),
                'en_proceso': depto_solicitudes.filter(estado='en_proceso').count(),
                'finalizadas': depto_solicitudes.filter(estado='finalizada').count(),
            })
        
        # Métricas
        metrics = {
            'total_solicitudes': solicitudes.count(),
            'pendientes': solicitudes.filter(estado='derivada').count(),
            'en_proceso': solicitudes.filter(estado='en_proceso').count(),
            'finalizadas': solicitudes.filter(estado='finalizada').count(),
        }
        
        context = {
            'metrics': metrics,
            'solicitudes_por_departamento': solicitudes_por_departamento,
            'perfil': 'Dirección'
        }
        return render(request, 'core/dashboard_direccion.html', context)
        
    except Exception as e:
        messages.error(request, f'Error al cargar dashboard: {str(e)}')
        return redirect('check_profile')

@login_required
def dashboard_departamento(request):
    if request.user.profile.perfil != 'departamento':
        messages.error(request, 'Acceso denegado')
        return redirect('check_profile')
    
    # Obtener departamentos del usuario
    departamentos_usuario = Departamento.objects.filter(
        Q(nombre_encargado=request.user.get_full_name()) | 
        Q(correo_encargado=request.user.email)
    )
    
    solicitudes = Solicitud.objects.filter(departamento_asignado__in=departamentos_usuario)
    solicitudes_sin_asignar = solicitudes.filter(estado='derivada', cuadrilla_asignada__isnull=True)
    
    metrics = {
        'total_solicitudes': solicitudes.count(),
        'sin_asignar': solicitudes_sin_asignar.count(),
        'en_proceso': solicitudes.filter(estado='en_proceso').count(),
        'finalizadas': solicitudes.filter(estado='finalizada').count(),
    }
    
    context = {
        'metrics': metrics,
        'solicitudes_sin_asignar': solicitudes_sin_asignar,
        'perfil': 'Departamento'
    }
    return render(request, 'core/dashboard_departamento.html', context)

@login_required
def dashboard_cuadrilla(request):
    if request.user.profile.perfil != 'cuadrilla':
        messages.error(request, 'Acceso denegado')
        return redirect('check_profile')
    
    # Obtener cuadrillas del usuario
    cuadrillas_usuario = UsuarioCuadrilla.objects.filter(usuario=request.user).values_list('cuadrilla', flat=True)
    solicitudes = Solicitud.objects.filter(cuadrilla_asignada__in=cuadrillas_usuario)
    solicitudes_en_proceso = solicitudes.filter(estado='en_proceso')
    
    metrics = {
        'asignadas': solicitudes.count(),
        'pendientes': solicitudes.filter(estado='derivada').count(),
        'finalizadas': solicitudes.filter(estado='finalizada').count(),
    }
    
    context = {
        'metrics': metrics,
        'solicitudes_en_proceso': solicitudes_en_proceso,
        'perfil': 'Cuadrilla'
    }
    return render(request, 'core/dashboard_cuadrilla.html', context)
