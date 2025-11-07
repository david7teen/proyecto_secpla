from django.shortcuts import render, redirect
from .models import Usuario, Incidencia
from encuesta.forms import IncidenciaForm

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
    usuario_activo = Usuario.objects.get(id=request.session['usuario_activo']['id'])

    incidencias = Incidencia.objects.filter(territorial_creador=usuario_activo)

    # Obtener encuestas recientes
    encuestas = Encuesta.objects.filter(estado='Abierta').order_by('-id')[:3]

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

