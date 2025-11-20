from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
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


def vista_territorial(request):
    usuario_activo_data = request.session.get('usuario_activo')
    if not usuario_activo_data:
        return redirect('/secpla/login/territorial/')
    
    usuario_activo = Usuario.objects.get(id=usuario_activo_data['id'])

    incidencias = Incidencia.objects.filter(territorial_creador=usuario_activo)
    
    incidencias_recientes = incidencias.order_by('-fecha_creacion')[:5] 

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
        'incidencias': incidencias_recientes,
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
            pregunta_ids = request.POST.getlist('preguntas[]')
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

            encuesta.preguntas.set(preguntas_seleccionadas)

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

def crear_incidencia(request):
    usuario_activo_data = request.session.get('usuario_activo')
    if not usuario_activo_data:
        return redirect('/secpla/login/territorial/')
    
    usuario_activo = Usuario.objects.get(id=usuario_activo_data['id'])
    
    direcciones = Direccion.objects.filter(estado='Activo')
    tipos_incidencia = TipoIncidencia.objects.all()

    if request.method == 'POST':
        try:
            nombre_incidencia = request.POST.get('nombre_incidencia')
            descripcion = request.POST.get('descripcion')
            direccion_id = request.POST.get('direccion_incidencia')
            departamento_id = request.POST.get('departamento_incidencia')
            tipo_incidencia_id = request.POST.get('tipo_incidencia')
            prioridad = request.POST.get('prioridad')
            ubicacion = request.POST.get('ubicacion')
            datos_vecino_nombre = request.POST.get('datos_vecino_nombre')
            datos_vecino_celular = request.POST.get('datos_vecino_celular')
            datos_vecino_email = request.POST.get('datos_vecino_email')
            if datos_vecino_nombre or datos_vecino_celular or datos_vecino_email:
                datos_vecino = ' - '.join(filter(None, [datos_vecino_nombre or '', datos_vecino_celular or '', datos_vecino_email or '']))
            else:
                datos_vecino = request.POST.get('datos_vecino')
            imagen = request.FILES.get('imagen')

            if not all([nombre_incidencia, descripcion, direccion_id, departamento_id]):
                messages.error(request, 'Por favor complete todos los campos obligatorios.')
                return render(request, 'territorial/crear_incidencia.html', {
                    'usuario_activo': usuario_activo,
                    'direcciones': direcciones,
                    'departamentos': Departamento.objects.filter(estado='Activo'),
                    'tipos_incidencia': tipos_incidencia,
                })

            direccion = Direccion.objects.get(id=direccion_id)
            departamento = Departamento.objects.get(id=departamento_id)
            tipo_incidencia = TipoIncidencia.objects.get(id=tipo_incidencia_id) if tipo_incidencia_id else None

            incidencia = Incidencia.objects.create(
                nombre_incidencia=nombre_incidencia,
                descripcion=descripcion,
                direccion_incidencia=direccion,
                departamento_incidencia=departamento,
                tipo_incidencia=tipo_incidencia,
                prioridad=prioridad,
                ubicacion=ubicacion,
                datos_vecino=datos_vecino,
                imagen=imagen,
                territorial_creador=usuario_activo,
                estado='Abierta'
            )

            messages.success(request, 'Incidencia creada exitosamente.')
            return redirect('dashboard_territorial')

        except Exception as e:
            messages.error(request, f'Error al crear la incidencia: {str(e)}')
            departamentos = Departamento.objects.filter(estado='Activo')
            return render(request, 'territorial/crear_incidencia.html', {
                'usuario_activo': usuario_activo,
                'direcciones': direcciones,
                'departamentos': departamentos,
                'tipos_incidencia': tipos_incidencia,
            })

    departamentos = Departamento.objects.filter(estado='Activo')

    return render(request, 'territorial/crear_incidencia.html', {
        'usuario_activo': usuario_activo,
        'direcciones': direcciones,
        'departamentos': departamentos,
        'tipos_incidencia': tipos_incidencia,
    })
    
def editar_incidencia(request, incidencia_id):
    usuario_activo_data = request.session.get('usuario_activo')
    if not usuario_activo_data:
        return redirect('/secpla/login/territorial/')
    
    usuario_activo = Usuario.objects.get(id=usuario_activo_data['id'])
    incidencia = get_object_or_404(Incidencia, id=incidencia_id)

    if incidencia.estado not in ['Abierta', 'Rechazada']:
        messages.error(request, 'Solo puede editar incidencias en estado Abierta o Rechazada.')
        return redirect('dashboard_territorial')

    direcciones = Direccion.objects.filter(estado='Activo')
    tipos_incidencia = TipoIncidencia.objects.all()

    if request.method == 'POST':
        try:
            incidencia.nombre_incidencia = request.POST.get('nombre_incidencia')
            incidencia.descripcion = request.POST.get('descripcion')
            direccion_id = request.POST.get('direccion_incidencia')
            departamento_id = request.POST.get('departamento_incidencia')
            tipo_incidencia_id = request.POST.get('tipo_incidencia')
            incidencia.prioridad = request.POST.get('prioridad')
            incidencia.ubicacion = request.POST.get('ubicacion')
            datos_vecino_nombre = request.POST.get('datos_vecino_nombre')
            datos_vecino_celular = request.POST.get('datos_vecino_celular')
            datos_vecino_email = request.POST.get('datos_vecino_email')
            if datos_vecino_nombre or datos_vecino_celular or datos_vecino_email:
                incidencia.datos_vecino = ' - '.join(filter(None, [datos_vecino_nombre or '', datos_vecino_celular or '', datos_vecino_email or '']))
            else:
                incidencia.datos_vecino = request.POST.get('datos_vecino')

            if 'imagen' in request.FILES:
                incidencia.imagen = request.FILES['imagen']

            if direccion_id:
                incidencia.direccion_incidencia = Direccion.objects.get(id=direccion_id)
            if departamento_id:
                incidencia.departamento_incidencia = Departamento.objects.get(id=departamento_id)
            if tipo_incidencia_id:
                incidencia.tipo_incidencia = TipoIncidencia.objects.get(id=tipo_incidencia_id)

            if incidencia.estado == 'Rechazada':
                incidencia.estado = 'Abierta'

            incidencia.save()
            messages.success(request, 'Incidencia actualizada exitosamente.')
            return redirect('dashboard_territorial')

        except Exception as e:
            messages.error(request, f'Error al actualizar la incidencia: {str(e)}')

    departamentos = Departamento.objects.filter(
        direccion_departamento=incidencia.direccion_incidencia, 
        estado='Activo'
    )

    datos_vecino_nombre = datos_vecino_celular = datos_vecino_email = ''
    if incidencia.datos_vecino:
        parts = [p.strip() for p in incidencia.datos_vecino.split(' - ')]
        if len(parts) >= 1:
            datos_vecino_nombre = parts[0]
        if len(parts) >= 2:
            datos_vecino_celular = parts[1]
        if len(parts) >= 3:
            datos_vecino_email = parts[2]

    return render(request, 'territorial/editar_incidencia.html', {
        'usuario_activo': usuario_activo,
        'incidencia': incidencia,
        'direcciones': direcciones,
        'departamentos': departamentos,
        'tipos_incidencia': tipos_incidencia,
        'datos_vecino_nombre': datos_vecino_nombre,
        'datos_vecino_celular': datos_vecino_celular,
        'datos_vecino_email': datos_vecino_email,
    })

def eliminar_incidencia(request, incidencia_id):
    usuario_activo_data = request.session.get('usuario_activo')
    if not usuario_activo_data:
        return redirect('/secpla/login/territorial/')
    
    usuario_activo = Usuario.objects.get(id=usuario_activo_data['id'])
    incidencia = get_object_or_404(Incidencia, id=incidencia_id, territorial_creador=usuario_activo)

    if incidencia.estado != 'Abierta':
        messages.error(request, 'Solo puede eliminar incidencias en estado Abierta.')
        return redirect('dashboard_territorial')

    if request.method == 'POST':
        incidencia.delete()
        messages.success(request, 'Incidencia eliminada exitosamente.')
        return redirect('dashboard_territorial')

    return render(request, 'territorial/eliminar_incidencia.html', {
        'usuario_activo': usuario_activo,
        'incidencia': incidencia,
    })


def obtener_departamentos_por_direccion(request, direccion_id):
    try:
        departamentos = Departamento.objects.filter(
            direccion_departamento_id=direccion_id, 
            estado='Activo'
        )
        data = [{'id': d.id, 'nombre': d.nombre_departamento} for d in departamentos]
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


def listar_incidencias_territorial(request):
    usuario_activo_data = request.session.get('usuario_activo')
    if not usuario_activo_data:
        return redirect('/secpla/login/territorial/')
    
    usuario_activo = Usuario.objects.get(id=usuario_activo_data['id'])
    
    incidencias_list = Incidencia.objects.filter(territorial_creador=usuario_activo).order_by('-fecha_creacion')
    
    estado_filtro = request.GET.get('estado')
    if estado_filtro:
        incidencias_list = incidencias_list.filter(estado=estado_filtro)
    
    estado_choices = Incidencia._meta.get_field('estado').choices

    return render(request, 'territorial/listar_incidencias_territorial.html', {
        'usuario_activo': usuario_activo,
        'incidencias': incidencias_list,
        'estado_choices': estado_choices,
        'estado_filtro': estado_filtro
    })
