from django.shortcuts import render, redirect

from SECPLA.models import Usuario
from incidencia.models import Incidencia
from departamento.models import Departamento
from direccion.models import Direccion
from pregunta.models import Pregunta
from tipo_incidencia.models import TipoIncidencia
from encuesta.models import Encuesta
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from territorial.models import Territorial
from django.shortcuts import get_object_or_404


def vista_territorial(request):
    usuario_activo_data = request.session.get('usuario_activo')
    if not usuario_activo_data:
        return redirect('/secpla/login/territorial/')
    
    usuario_activo = Usuario.objects.get(id=usuario_activo_data['id'])

    incidencias = Incidencia.objects.filter(territorial_creador=usuario_activo)
    incidencias_abiertas = incidencias.filter(estado='Abierta')[:5]  # Últimas 5

    encuestas = Encuesta.objects.filter(estado='Abierta').order_by('-id')[:5]

    resumen = {
        'abiertas': incidencias.filter(estado='Abierta').count(),
        'derivadas': incidencias.filter(estado='Derivada').count(),
        'rechazadas': incidencias.filter(estado='Rechazada').count(),
        'proceso': incidencias.filter(estado='En proceso').count(),
        'finalizadas': incidencias.filter(estado='Finalizada').count(),
        'cerradas': incidencias.filter(estado='Cerrada').count(),
        'total': incidencias.count()
    }

    return render(request, 'Territorial/dashboard_territorial.html', {
        'usuario_activo': usuario_activo,
        'resumen': resumen,
        'encuestas': encuestas,
        'incidencias_abiertas': incidencias_abiertas
    })

def obtener_departamentos_por_direccion(request, direccion_id):
    departamentos = Departamento.objects.filter(direccion_departamento_id=direccion_id, estado='Activo')
    data = [{'id': d.id, 'nombre': d.nombre_departamento} for d in departamentos]
    return JsonResponse(data, safe=False)

def responder_preguntas_encuesta(request):
    if request.session.get('perfil') != 'SECPLA':
        return redirect('/login/secpla/')

    preguntas = Pregunta.objects.all()
    incidencias = TipoIncidencia.objects.all()
    direcciones = Direccion.objects.filter(estado='Activo')

    if request.method == 'POST':
        try:
            nombre = request.POST.get('nombre_encuesta')
            descripcion = request.POST.get('descripcion_incidente')
            ubicacion = request.POST.get('ubicacion')
            imagen = request.FILES.get('imagen')
            video = request.FILES.get('video')
            audio = request.FILES.get('audio')

            prioridad = request.POST.get('prioridad')
            datos_vecino = request.POST.get('datos_vecino')
            incidencia_id = request.POST.get('tipo_incidencia')
            pregunta_ids = request.POST.getlist('preguntas[]')  # ✅ lista de IDs

            if not all([nombre, prioridad, incidencia_id]):
                raise ValueError("Faltan campos obligatorios.")

            incidencia = TipoIncidencia.objects.get(id=incidencia_id)
            preguntas_seleccionadas = Pregunta.objects.filter(id__in=pregunta_ids)

            encuesta = Encuesta.objects.create(
                nombre_encuesta=nombre,
                descripcion_incidente=descripcion,
                ubicacion=ubicacion,
                imagen=imagen,
                video=video,
                audio=audio,
                prioridad=prioridad,
                datos_vecino=datos_vecino,
                tipo_incidencia=incidencia,
                estado='Activo',
                categoria='Vigente'
            )

            encuesta.preguntas.set(preguntas_seleccionadas)  # ✅ asigna todas las preguntas

            return redirect('vista_secpla')

        except Exception as e:
            return render(request, 'SECPLA/crear_encuesta.html', {
                'error': str(e),
                'preguntas': preguntas,
                'incidencias': incidencias,
                'direcciones': direcciones
            })

    return render(request, 'SECPLA/crear_encuesta.html', {
        'preguntas': preguntas,
        'incidencias': incidencias,
        'direcciones': direcciones
    })

@require_POST
def derivar_encuesta(request, id):
    encuesta = get_object_or_404(Encuesta, id=id)
    if request.session.get('perfil') != 'TERRITORIAL':
        return redirect('/login/territorial/')
    if encuesta.estado != 'Abierta':
        return redirect('dashboard_territorial')
    
    # Validar que las preguntas estén respondidas (si aplica)
    encuesta.estado = 'Derivada'
    encuesta.save()
    return redirect('dashboard_territorial')


def encuestas_abiertas(request):
    if request.session.get('perfil') != 'Territorial':
        return redirect('/login/territorial/')
    
    encuestas = Encuesta.objects.filter(estado='Abierta').order_by('-id')
    
    return render(request, 'territorial/encuestas_abiertas.html', {
        'encuestas': encuestas,
        'perfil': 'territorial'
    })

def incidencias_abiertas(request):
    usuario_activo_data = request.session.get('usuario_activo')
    if not usuario_activo_data:
        return redirect('/secpla/login/territorial/')
    
    usuario_activo = Usuario.objects.get(id=usuario_activo_data['id'])
    abiertas = Incidencia.objects.filter(territorial_creador=usuario_activo, estado='Abierta')
    
    return render(request, 'territorial/listado_incidencias.html', {
        'incidencias': abiertas,
        'estado': 'Abiertas',
        'usuario_activo': usuario_activo
    })

def incidencias_derivadas(request):
    usuario_activo_data = request.session.get('usuario_activo')
    if not usuario_activo_data:
        return redirect('/secpla/login/territorial/')
    
    usuario_activo = Usuario.objects.get(id=usuario_activo_data['id'])
    derivadas = Incidencia.objects.filter(territorial_creador=usuario_activo, estado='Derivada')
    
    return render(request, 'territorial/listado_incidencias.html', {
        'incidencias': derivadas,
        'estado': 'Derivadas',
        'usuario_activo': usuario_activo
    })

def incidencias_proceso(request):
    usuario_activo_data = request.session.get('usuario_activo')
    if not usuario_activo_data:
        return redirect('/secpla/login/territorial/')
    
    usuario_activo = Usuario.objects.get(id=usuario_activo_data['id'])
    proceso = Incidencia.objects.filter(territorial_creador=usuario_activo, estado='En proceso')
    
    return render(request, 'territorial/listado_incidencias.html', {
        'incidencias': proceso,
        'estado': 'En Proceso',
        'usuario_activo': usuario_activo
    })

def incidencias_rechazadas(request):
    usuario_activo_data = request.session.get('usuario_activo')
    if not usuario_activo_data:
        return redirect('/secpla/login/territorial/')
    
    usuario_activo = Usuario.objects.get(id=usuario_activo_data['id'])
    rechazadas = Incidencia.objects.filter(territorial_creador=usuario_activo, estado='Rechazada')
    
    return render(request, 'territorial/listado_incidencias.html', {
        'incidencias': rechazadas,
        'estado': 'Rechazadas',
        'usuario_activo': usuario_activo
    })

def incidencias_finalizadas(request):
    usuario_activo_data = request.session.get('usuario_activo')
    if not usuario_activo_data:
        return redirect('/secpla/login/territorial/')
    
    usuario_activo = Usuario.objects.get(id=usuario_activo_data['id'])
    finalizadas = Incidencia.objects.filter(territorial_creador=usuario_activo, estado='Finalizada')
    
    return render(request, 'territorial/listado_incidencias.html', {
        'incidencias': finalizadas,
        'estado': 'Finalizadas',
        'usuario_activo': usuario_activo
    })

def incidencias_cerradas(request):
    usuario_activo_data = request.session.get('usuario_activo')
    if not usuario_activo_data:
        return redirect('/secpla/login/territorial/')
    
    usuario_activo = Usuario.objects.get(id=usuario_activo_data['id'])
    cerradas = Incidencia.objects.filter(territorial_creador=usuario_activo, estado='Cerrada')
    
    return render(request, 'territorial/listado_incidencias.html', {
        'incidencias': cerradas,
        'estado': 'Cerradas',
        'usuario_activo': usuario_activo
    })

def ver_todas_solicitudes(request):
    usuario_activo_data = request.session.get('usuario_activo')
    if not usuario_activo_data:
        return redirect('/secpla/login/territorial/')
    
    usuario_activo = Usuario.objects.get(id=usuario_activo_data['id'])
    todas = Incidencia.objects.filter(territorial_creador=usuario_activo)
    
    return render(request, 'territorial/listado_incidencias.html', {
        'incidencias': todas,
        'estado': 'Todas las Solicitudes',
        'usuario_activo': usuario_activo
    })
