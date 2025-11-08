from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from SECPLA.models import Usuario
from incidencia.models import Incidencia 
from direccion.models import Direccion
from departamento.models import Departamento
from django.http import JsonResponse
from encuesta.models import Encuesta
from territorial.models import Territorial
from django.views.decorators.http import require_POST
from encuesta.models import Pregunta
from .models import RecuperacionIntento
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.contrib import messages
from tipo_incidencia.models import TipoIncidencia
from django.db import IntegrityError


redirecciones = {
    'secpla': 'SECPLA',
    'direccion': 'Dirección',
    'departamento': 'Departamento',
    'territorial': 'Territorial',
    'cuadrilla': 'Cuadrilla'
}

from django.shortcuts import redirect

def salir_secpla(request):
    return redirect('/')

def login_usuario(request):
    if request.method == 'POST':
        correo = request.POST.get('correo')
        perfil = request.POST.get('perfil')
        usuario = Usuario.objects.filter(correo=correo, perfil=perfil, estado='Activo').first()
        if usuario:
            request.session['usuario_id'] = usuario.id
            request.session['perfil'] = usuario.perfil
            request.session['correo'] = usuario.correo
            return redirect(f'/perfil/{usuario.perfil.lower()}/')
        else:
            return render(request, 'SECPLA/login.html', {'error': 'Usuario no encontrado o perfil incorrecto'})
    return render(request, 'SECPLA/login.html')

def login_por_perfil(request, perfil):
    perfil_original = perfil.lower()
    perfil = redirecciones.get(perfil_original, perfil_original.capitalize())

    if request.method == 'POST':
        correo = request.POST.get('correo').strip().lower()
        contraseña = request.POST.get('contraseña').strip()

        usuario = Usuario.objects.filter(correo=correo, perfil=perfil).first()

        if not usuario:
            error = 'No existe una cuenta con ese correo y perfil.'
        elif usuario.estado != 'Activo':
            error = 'Tu cuenta ha sido bloqueada por el administrador.'
        elif usuario.contraseña.strip() != contraseña:
            error = 'Contraseña incorrecta.'
        else:
            # Login exitoso - CORREGIDO
            request.session['usuario_activo'] = {
                'id': usuario.id,
                'nombre': usuario.nombre,
                'apellido': usuario.apellido,
                'correo': usuario.correo,
                'perfil': usuario.perfil
            }
            request.session['usuario_id'] = usuario.id
            request.session['perfil'] = usuario.perfil
            request.session['correo'] = usuario.correo
            return redirect(f"/perfil/{perfil_original}/")

        return render(request, 'SECPLA/login.html', {
            'error': error,
            'perfil': perfil_original
        })

    return render(request, 'SECPLA/login.html', {'perfil': perfil_original})

def vista_secpla(request):
    if request.session.get('perfil') != 'SECPLA':
        perfil = request.session.get('perfil')
        return redirect(f"/perfil/{redirecciones.get(perfil, perfil.lower())}/")

    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('/login/secpla/')

    try:
        usuario_activo = Usuario.objects.get(id=usuario_id)
    except Usuario.DoesNotExist:
        return redirect('/login/secpla/')

    usuarios = Usuario.objects.all().order_by('-id')[:3]
    direcciones = Direccion.objects.filter(estado='Activo').order_by('-id')[:3]
    departamentos = Departamento.objects.filter(estado='Activo').order_by('-id')[:3]
    territoriales = Territorial.objects.filter(estado='Activo').order_by('-id')[:3]
    incidencias = Incidencia.objects.all().order_by('-id')[:3]
    encuestas = Encuesta.objects.all().order_by('-id')[:3]

    resumen = {
        'usuarios_activos': Usuario.objects.filter(estado='Activo').count(),
        'direcciones_creadas': Direccion.objects.filter(estado='Activo').count(),
        'departamentos_creados': Departamento.objects.filter(estado='Activo').count(),
        'territoriales': Territorial.objects.filter( estado='Activo').count(),
        'incidencias_creadas':Incidencia.objects.filter(estado='Activo').count(),
        'derivadas': Incidencia.objects.filter(estado='Derivada').count(),
        'rechazadas': Incidencia.objects.filter(estado='Rechazada').count(),
        'finalizadas': Incidencia.objects.filter(estado='Finalizada').count(),
    }

    return render(request, 'SECPLA/dashboard_secpla.html', {
        'usuario_activo': usuario_activo,
        'usuarios': usuarios,
        'direcciones': direcciones,
        'departamentos':departamentos,
        'incidencias':incidencias,
        'encuestas':encuestas,
        'resumen': resumen,
        'perfil':'SECPLA',
    })

def vista_direccion(request):
    if request.session.get('perfil') != 'Dirección':
        perfil = request.session.get('perfil')
        return redirect(f"/perfil/{redirecciones.get(perfil, perfil.lower())}/")
    return render(request, 'direccion/dashboard_direccion.html',{
        'perfil':'Direccion',
    })

def vista_departamento(request):
    if request.session.get('perfil') != 'Departamento':
        perfil = request.session.get('perfil')
        return redirect(f"/perfil/{redirecciones.get(perfil, perfil.lower())}/")
    return render(request, 'departamento/dashboard_departamento.html',{
        'perfil':'Departamento',
    })

def vista_territorial(request):
    if request.session.get('perfil') != 'Territorial':
        perfil = request.session.get('perfil')
        return redirect(f"/perfil/{redirecciones.get(perfil, perfil.lower())}/")
    return render(request, 'territorial/dashboard_territorial.html',{
        'perfil':'Territorial',
    })

def vista_cuadrilla(request):
    if request.session.get('perfil') != 'Cuadrilla':
        perfil = request.session.get('perfil')
        return redirect(f"/perfil/{redirecciones.get(perfil, perfil.lower())}/")
    return render(request, 'cuadrilla/dashboard_cuadrilla.html',{
        'perfil':'Cuadrilla',
    })

def crear_usuario(request):
    if request.session.get('perfil') != 'SECPLA':
        return redirect('/login/secpla/')

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        correo = request.POST.get('correo')
        telefono = request.POST.get('telefono')
        perfil = request.POST.get('perfil')
        contraseña = request.POST.get('contraseña')

        Usuario.objects.create(
            nombre=nombre,
            apellido=apellido,
            correo=correo,
            telefono=telefono,
            perfil=perfil,
            contraseña=contraseña,
            estado='Activo'
        )
        return redirect('/secpla/dashboard/')

    return render(request, 'SECPLA/crear_usuario.html')

def dashboard_secpla(request):
    correo = request.session.get('correo')
    if not correo:
        return redirect('/login/secpla/')

    try:
        usuario_activo = Usuario.objects.get(correo=correo)
    except Usuario.DoesNotExist:
        return redirect('/login/secpla/')

    # Usuarios por perfil
    usuarios = Usuario.objects.all().order_by('perfil')
    direcciones = Usuario.objects.filter(perfil='Dirección').order_by('nombre')
    departamentos = Usuario.objects.filter(perfil='Departamento').order_by('nombre')
    territoriales = Usuario.objects.filter(perfil='Territorial').order_by('nombre')

    # Otros modelos
    incidencias = Incidencia.objects.all().order_by('-id')
    encuestas = Encuesta.objects.all().order_by('nombre_encuesta')

    # Resumen dinámico
    resumen = {
        'usuarios_activos': Usuario.objects.filter(estado='Activo').count(),
        'direcciones_creadas': Usuario.objects.filter(perfil='Dirección', estado='Activo').count(),
        'departamentos_creados': Usuario.objects.filter(perfil='Departamento', estado='Activo').count(),
        'territoriales': Usuario.objects.filter(perfil='Territorial', estado='Activo').count(),
        'incidencias_creadas': Incidencia.objects.count(),
        'derivadas': Incidencia.objects.filter(estado='Derivada').count(),
        'rechazadas': Incidencia.objects.filter(estado='Rechazada').count(),
        'finalizadas': Incidencia.objects.filter(estado='Finalizada').count(),
    }

    return render(request, 'SECPLA/dashboard_secpla.html', {
        'usuario_activo': usuario_activo,
        'usuarios': usuarios,
        'direcciones': direcciones,
        'departamentos': departamentos,
        'territoriales': territoriales,
        'incidencias': incidencias,
        'encuestas': encuestas,
        'resumen': resumen,
    })

def crear_direccion(request):
    if request.session.get('perfil') != 'SECPLA':
        return redirect('/login/secpla/')

    if request.method == 'POST':
        nombre_direccion = request.POST.get('nombre_direccion')
        nombre_encargado = request.POST.get('nombre_encargado')
        correo_encargado = request.POST.get('correo_encargado')

        Direccion.objects.create(
            nombre_direccion=nombre_direccion,
            nombre_encargado=nombre_encargado,
            correo_encargado=correo_encargado,
            estado='Activo'
        )
        return redirect('/perfil/secpla/')

    return render(request,'SECPLA/crear_direccion.html')

def crear_departamento(request):
    if request.session.get('perfil') != 'SECPLA':
        return redirect('/login/secpla/')

    direcciones_disponibles = Direccion.objects.filter(estado='Activo')

    if not direcciones_disponibles.exists():
        return render(request, 'SECPLA/crear_departamento.html', {
            'error': 'No hay direcciones disponibles. Cree una dirección primero.',
            'direcciones': []
        })

    if request.method == 'POST':
        nombre_departamento = request.POST.get('nombre_departamento')
        nombre_encargado = request.POST.get('nombre_encargado')
        correo_encargado = request.POST.get('correo_encargado')
        direccion_id = request.POST.get('direccion_departamento')

        try:
            direccion = Direccion.objects.get(id=direccion_id)
        except Direccion.DoesNotExist:
            return render(request, 'SECPLA/crear_departamento.html', {
                'error': 'La dirección seleccionada no existe.',
                'direcciones': direcciones_disponibles
            })

        Departamento.objects.create(
            nombre_departamento=nombre_departamento,
            encargado_departamento=nombre_encargado,
            correo_encargado=correo_encargado,
            direccion_departamento=direccion,
            estado='Activo'
        )
        return redirect('/perfil/secpla/')

    return render(request, 'SECPLA/crear_departamento.html', {
        'direcciones': direcciones_disponibles
    })


def crear_incidencia(request):
    if request.session.get('perfil') != 'SECPLA':
        print("Redirigiendo: perfil no es SECPLA")
        return redirect('/login/secpla/')

    direcciones_disponibles = Direccion.objects.filter(estado='Activo')

    if not direcciones_disponibles.exists():
        print("No hay direcciones disponibles")
        return render(request, 'SECPLA/crear_incidencia.html', {
            'error': 'No hay direcciones disponibles. Cree una dirección primero.',
            'direcciones': [],
            'departamentos': []
        })

    if request.method == 'POST':
        nombre_incidencia = request.POST.get('nombre_incidencia')
        descripcion = request.POST.get('descripcion')
        direccion_incidencia = request.POST.get('direccion_incidencia')
        departamento_incidencia = request.POST.get('departamento_incidencia')

        print(f"Datos recibidos: {nombre_incidencia}, {descripcion}, {direccion_incidencia}, {departamento_incidencia}")

        try:
            direccion = Direccion.objects.get(id=direccion_incidencia, estado='Activo')
        except Direccion.DoesNotExist:
            print("Dirección inválida")
            return render(request, 'SECPLA/crear_incidencia.html', {
                'error': 'La dirección seleccionada no existe.',
                'direcciones': direcciones_disponibles,
                'departamentos': []
            })

        departamentos_disponibles = Departamento.objects.filter(
            direccion_departamento=direccion,
            estado='Activo'
        )

        if not departamentos_disponibles.exists():
            print("No hay departamentos disponibles para esta dirección")
            return render(request, 'SECPLA/crear_incidencia.html', {
                'error': 'No hay departamentos asociados a esta dirección.',
                'direcciones': direcciones_disponibles,
                'departamentos': []
            })

        try:
            departamento = Departamento.objects.get(id=departamento_incidencia, direccion_departamento=direccion)
        except Departamento.DoesNotExist:
            print("Departamento inválido")
            return render(request, 'SECPLA/crear_incidencia.html', {
                'error': 'El departamento seleccionado no pertenece a la dirección elegida.',
                'direcciones': direcciones_disponibles,
                'departamentos': departamentos_disponibles
            })

        Incidencia.objects.create(
            nombre_incidencia=nombre_incidencia,
            descripcion=descripcion,
            direccion_incidencia=direccion,
            departamento_incidencia=departamento,
            estado='Activo'
        )
        print("Incidencia creada correctamente")
        return redirect('/perfil/secpla/')

    return render(request, 'SECPLA/crear_incidencia.html', {
        'direcciones': direcciones_disponibles,
        'departamentos': []
    })

def obtener_departamentos_por_direccion(request, direccion_id):
    departamentos = Departamento.objects.filter(direccion_departamento_id=direccion_id, estado='Activo')
    data = [{'id': d.id, 'nombre': d.nombre_departamento} for d in departamentos]
    return JsonResponse(data, safe=False)

def crear_encuesta(request):
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
                estado='Abierta',
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
def crear_pregunta_ajax(request):
    nombre = request.POST.get('nombre_pregunta', '').strip()
    if nombre:
        pregunta = Pregunta.objects.create(nombre_pregunta=nombre)
        return JsonResponse({'id': pregunta.id, 'nombre': pregunta.nombre_pregunta})
    return JsonResponse({'error': 'Nombre inválido'}, status=400)

def crear_pregunta_desde_encuesta(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre_pregunta')
        if nombre:
            nueva = Pregunta.objects.create(nombre_pregunta=nombre)
            return redirect('crear_encuesta')  # vuelve al formulario original
        return render(request, 'SECPLA/crear_pregunta_desde_encuesta.html', {'error': 'Campo vacío'})
    return render(request, 'SECPLA/crear_pregunta_desde_encuesta.html')

""""
def crear_territorial(request):
    if request.session.get('perfil') != 'SECPLA':
        return redirect('/login/secpla/')

    if request.method == 'POST':
        nombre = request.POST.get('nombre_territorial')
        apellido = request.POST.get('apellido_territorial')
        correo = request.POST.get('correo_territorial')
        telefono = request.POST.get('telefono_territorial')

        Territorial.objects.create(
            nombre_territorial=nombre,
            apellido_territorial=apellido,
            correo_territorial=correo,
            telefono_territorial=telefono,
            estado='Activo'
        )
        return redirect('/perfil/secpla/')

    return render(request, 'SECPLA/crear_territorial.html')
"""
def recuperar_cuenta(request):
    perfil = request.GET.get('perfil', 'SECPLA')
    mensaje = None

    if request.method == 'POST':
        correo = request.POST.get('correo')
        perfil = request.POST.get('perfil')

        usuario = Usuario.objects.filter(correo__iexact=correo, perfil__iexact=perfil).first()

        # Registrar el intento
        RecuperacionIntento.objects.create(
            correo=correo,
            perfil=perfil,
            estado='Pendiente',
            observacion='Solicitud iniciada desde formulario web'
        )

        if usuario:
            mensaje = "Se ha registrado tu solicitud. El equipo de SECPLA revisará tu cuenta."
        else:
            mensaje = "No se encontró una cuenta con ese correo y perfil. Tu solicitud fue registrada para revisión."

    return render(request, 'SECPLA/recuperar_cuenta.html', {
        'perfil': perfil,
        'mensaje': mensaje
    })


def ver_intentos_recuperacion(request):
    intentos = RecuperacionIntento.objects.all().order_by('-fecha')
    return render(request, 'SECPLA/ver_intentos_recuperacion.html', {
        'intentos': intentos
    })

def actualizar_estado_recuperacion(request, intento_id):
    intento = RecuperacionIntento.objects.get(id=intento_id)
    nuevo_estado = request.POST.get('estado')
    intento.estado = nuevo_estado
    intento.save()
    return redirect('ver_intentos_recuperacion')


def cambiar_contraseña(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)

    if request.method == 'POST':
        nueva_contraseña = request.POST.get('nueva_contraseña')
        confirmar = request.POST.get('confirmar_contraseña')

        if nueva_contraseña == confirmar:
            usuario.contraseña = nueva_contraseña  # Si usás hash, aplicalo aquí
            usuario.save()
            messages.success(request, 'Contraseña actualizada correctamente.')
            return redirect('ver_usuarios_secpla')  # O donde quieras redirigir
        else:
            messages.error(request, 'Las contraseñas no coinciden.')

    return render(request, 'SECPLA/cambiar_contraseña.html', {
        'usuario': usuario
    })

def ver_usuario(request):
    if request.session.get('perfil') != 'SECPLA':
        perfil = request.session.get('perfil')
        return redirect(f"/perfil/{redirecciones.get(perfil, perfil.lower())}/")

    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('/login/secpla/')

    try:
        usuario_activo = Usuario.objects.get(id=usuario_id)
    except Usuario.DoesNotExist:
        return redirect('/login/secpla/')

    usuarios = Usuario.objects.all().order_by('-id')
    resumen = {
        'usuarios_activos': Usuario.objects.filter(estado='Activo').count(),
    }

    return render(request, 'SECPLA/ver_usuario.html', {
        'usuario_activo': usuario_activo,
        'usuarios': usuarios,
        'resumen': resumen,
        'perfil':'SECPLA',
    })

def ver_usuario_2(request, usuario_id):
    if request.session.get('perfil') != 'SECPLA':
        return redirect('/login/secpla/')
    usuario = get_object_or_404(Usuario, id=usuario_id)
    return render(request, 'SECPLA/ver_usuario_2.html', {'usuario': usuario})

def editar_usuario(request, usuario_id):
    if request.session.get('perfil') != 'SECPLA':
        return redirect('/login/secpla/')
    usuario = get_object_or_404(Usuario, id=usuario_id)

    if request.method == 'POST':
        usuario.nombre = request.POST.get('nombre')
        usuario.apellido = request.POST.get('apellido')
        usuario.correo = request.POST.get('correo')
        usuario.telefono = request.POST.get('telefono')
        usuario.perfil = request.POST.get('perfil')
        usuario.save()
        return redirect('vista_secpla')

    return render(request, 'SECPLA/editar_usuario.html', {'usuario': usuario})

def bloquear_usuario(request, usuario_id):
    if request.session.get('perfil') != 'SECPLA':
        return redirect('/login/secpla/')
    usuario = get_object_or_404(Usuario, id=usuario_id)
    usuario.estado = 'Inactivo'
    usuario.save()
    return redirect('vista_secpla')

def activar_usuario(request, usuario_id):
    if request.session.get('perfil') != 'SECPLA':
        return redirect('/login/secpla/')
    usuario = get_object_or_404(Usuario, id=usuario_id)
    usuario.estado = 'Activo'
    usuario.save()
    return redirect('vista_secpla')

def ver_direccion(request, id):
    if request.session.get('perfil') != 'SECPLA':
        return redirect('/login/secpla/')
    direccion = get_object_or_404(Direccion, id=id)
    return render(request, 'SECPLA/ver_direccion.html', {'direccion': direccion})

def editar_direccion(request, id):
    if request.session.get('perfil') != 'SECPLA':
        return redirect('/login/secpla/')
    direccion = get_object_or_404(Direccion, id=id)

    if request.method == 'POST':
        direccion.nombre_direccion = request.POST.get('nombre_direccion')
        direccion.nombre_encargado = request.POST.get('nombre_encargado')
        direccion.correo_encargado = request.POST.get('correo_encargado')
        direccion.estado = request.POST.get('estado')
        direccion.save()
        return redirect('vista_secpla')

    return render(request, 'SECPLA/editar_direccion.html', {'direccion': direccion})

def bloquear_direccion(request, id):
    if request.session.get('perfil') != 'SECPLA':
        return redirect('/login/secpla/')
    direccion = get_object_or_404(Direccion, id=id)
    direccion.estado = 'Inactivo'
    direccion.save()
    return redirect('vista_secpla')

def activar_direccion(request, id):
    if request.session.get('perfil') != 'SECPLA':
        return redirect('/login/secpla/')
    direccion = get_object_or_404(Direccion, id=id)
    direccion.estado = 'Activo'
    direccion.save()
    return redirect('vista_secpla')

def listar_direcciones(request):
    if request.session.get('perfil') != 'SECPLA':
        perfil = request.session.get('perfil')
        return redirect(f"/perfil/{redirecciones.get(perfil, perfil.lower())}/")

    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('/login/secpla/')

    try:
        usuario_activo = Usuario.objects.get(id=usuario_id)
    except Usuario.DoesNotExist:
        return redirect('/login/secpla/')

    direcciones = Direccion.objects.exclude(id__isnull=True).order_by('-id')
    resumen = {
        'direcciones_activas': Direccion.objects.filter(estado='Activo').count(),
    }

    return render(request, 'SECPLA/listar_direcciones.html', {
        'usuario_activo': usuario_activo,
        'direcciones': direcciones,
        'resumen': resumen,
        'perfil': 'SECPLA',
    })

def ver_departamento(request, id):
    if request.session.get('perfil') != 'SECPLA':
        return redirect('/login/secpla/')
    
    departamento = get_object_or_404(Departamento, id=id)
    
    return render(request, 'SECPLA/ver_departamento.html', {
        'departamento': departamento,
        'direccion': departamento.direccion_departamento  # si existe relación
    })

def editar_departamento(request, id):
    if request.session.get('perfil') != 'SECPLA':
        return redirect('/login/secpla/')
    
    departamento = get_object_or_404(Departamento, id=id)
    
    if request.method == 'POST':
        departamento.nombre_departamento = request.POST.get('nombre_departamento')
        departamento.nombre_encargado = request.POST.get('nombre_encargado')
        departamento.correo_encargado = request.POST.get('correo_encargado')
        direccion_id = request.POST.get('direccion_departamento')
        departamento.estado = request.POST.get('estado')

        if direccion_id:
            departamento.direccion_departamento = Direccion.objects.filter(id=direccion_id).first()
        
        departamento.save()
        return redirect('vista_secpla')
    
    direcciones = Direccion.objects.filter(estado='Activo')
    
    return render(request, 'SECPLA/editar_departamento.html', {
        'departamento': departamento,
        'direcciones': direcciones
    })

def bloquear_departamento(request, id):
    if request.session.get('perfil') != 'SECPLA':
        return redirect('/login/secpla/')
    
    departamento = get_object_or_404(Departamento, id=id)
    departamento.estado = 'Inactivo'
    departamento.save()
    
    return redirect('vista_secpla')

def activar_departamento(request, id):
    if request.session.get('perfil') != 'SECPLA':
        return redirect('/login/secpla/')
    
    departamento = get_object_or_404(Departamento, id=id)
    departamento.estado = 'Activo'
    departamento.save()
    
    return redirect('vista_secpla')

def listar_departamentos(request):
    if request.session.get('perfil') != 'SECPLA':
        perfil = request.session.get('perfil')
        return redirect(f"/perfil/{redirecciones.get(perfil, perfil.lower())}/")

    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('/login/secpla/')

    try:
        usuario_activo = Usuario.objects.get(id=usuario_id)
    except Usuario.DoesNotExist:
        return redirect('/login/secpla/')

    departamentos = Departamento.objects.exclude(id__isnull=True).order_by('nombre_departamento')
    resumen = {
        'departamentos_activos': Departamento.objects.filter(estado='Activo').count(),
    }

    return render(request, 'SECPLA/listar_departamentos.html', {
        'usuario_activo': usuario_activo,
        'departamentos': departamentos,
        'resumen': resumen,
        'perfil': 'SECPLA',
    })

def ver_incidencia(request, incidencia_id):
    if request.session.get('perfil') != 'SECPLA':
        return redirect('/login/secpla/')
    
    incidencia = get_object_or_404(Incidencia, id=incidencia_id)
    
    return render(request, 'SECPLA/ver_incidencia.html', {
        'incidencia': incidencia
    })

def editar_incidencia(request, incidencia_id):
    if request.session.get('perfil') != 'SECPLA':
        return redirect('/login/secpla/')
    
    incidencia = get_object_or_404(Incidencia, id=incidencia_id)
    
    if request.method == 'POST':
        incidencia.nombre_incidencia = request.POST.get('nombre_incidencia')
        incidencia.descripcion = request.POST.get('descripcion')
        incidencia.estado = request.POST.get('estado')

        direccion_id = request.POST.get('direccion_incidencia')
        departamento_id = request.POST.get('departamento_incidencia')

        if direccion_id:
            incidencia.direccion_incidencia = Direccion.objects.filter(id=direccion_id).first()
        if departamento_id:
            incidencia.departamento_incidencia = Departamento.objects.filter(id=departamento_id).first()

        incidencia.save()
        return redirect('listar_incidencias')

    direcciones = Direccion.objects.filter(estado='Activo')
    departamentos = Departamento.objects.filter(estado='Activo')

    return render(request, 'SECPLA/editar_incidencia.html', {
        'incidencia': incidencia,
        'direcciones': direcciones,
        'departamentos': departamentos
    })

def activar_incidencia(request, incidencia_id):
    if request.session.get('perfil') != 'SECPLA':
        return redirect('/login/secpla/')
    
    incidencia = get_object_or_404(Incidencia, id=incidencia_id)
    incidencia.estado = 'Activo'
    incidencia.save()
    
    return redirect('listar_incidencias')

def bloquear_incidencia(request, incidencia_id):
    if request.session.get('perfil') != 'SECPLA':
        return redirect('/login/secpla/')
    
    incidencia = get_object_or_404(Incidencia, id=incidencia_id)
    incidencia.estado = 'Inactivo'
    incidencia.save()
    
    return redirect('listar_incidencias')

def listar_incidencias(request):
    if request.session.get('perfil') != 'SECPLA':
        perfil = request.session.get('perfil')
        return redirect(f"/perfil/{redirecciones.get(perfil, perfil.lower())}/")

    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('/login/secpla/')

    try:
        usuario_activo = Usuario.objects.get(id=usuario_id)
    except Usuario.DoesNotExist:
        return redirect('/login/secpla/')

    incidencias = Incidencia.objects.exclude(id__isnull=True).order_by('-id')
    resumen = {
        'incidencias_activas': Incidencia.objects.filter(estado='Activo').count(),
    }

    return render(request, 'SECPLA/listar_incidencias.html', {
        'usuario_activo': usuario_activo,
        'incidencias': incidencias,
        'resumen': resumen,
        'perfil': 'SECPLA',
    })

def ver_encuesta(request, encuesta_id):
    if request.session.get('perfil') != 'SECPLA':
        return redirect('/login/secpla/')
    
    encuesta = get_object_or_404(Encuesta, id=encuesta_id)
    
    return render(request, 'SECPLA/ver_encuesta.html', {
        'encuesta': encuesta
    })

def editar_encuesta(request, encuesta_id):
    if request.session.get('perfil') != 'SECPLA':
        return redirect('/login/secpla/')
    
    encuesta = get_object_or_404(Encuesta, id=encuesta_id)
    
    if request.method == 'POST':
        encuesta.nombre_encuesta = request.POST.get('nombre_encuesta')
        encuesta.descripcion_incidente = request.POST.get('descripcion_incidente')
        encuesta.ubicacion = request.POST.get('ubicacion')
        encuesta.prioridad = request.POST.get('prioridad')
        encuesta.datos_vecino = request.POST.get('datos_vecino')

        pregunta_id = request.POST.get('pregunta')
        incidencia_id = request.POST.get('tipo_incidencia')

        if pregunta_id:
            encuesta.pregunta = Pregunta.objects.filter(id=pregunta_id).first()
        if incidencia_id:
            encuesta.tipo_incidencia = Incidencia.objects.filter(id=incidencia_id).first()

        if 'imagen' in request.FILES:
            encuesta.imagen = request.FILES['imagen']
        if 'video' in request.FILES:
            encuesta.video = request.FILES['video']
        if 'audio' in request.FILES:
            encuesta.audio = request.FILES['audio']

        encuesta.save()
        return redirect('listar_encuestas')

    preguntas = Pregunta.objects.all()
    incidencias = Incidencia.objects.all()

    return render(request, 'SECPLA/editar_encuesta.html', {
        'encuesta': encuesta,
        'preguntas': preguntas,
        'incidencias': incidencias
    })

def activar_encuesta(request, encuesta_id):
    if request.session.get('perfil') != 'SECPLA':
        return redirect('/login/secpla/')
    
    encuesta = get_object_or_404(Encuesta, id=encuesta_id)
    encuesta.categoria = 'Vigente'
    encuesta.save()
    
    return redirect('listar_encuestas')

def bloquear_encuesta(request, encuesta_id):
    if request.session.get('perfil') != 'SECPLA':
        return redirect('/login/secpla/')
    
    encuesta = get_object_or_404(Encuesta, id=encuesta_id)
    encuesta.categoria = 'Bloqueada'
    encuesta.save()
    
    return redirect('listar_encuestas')


def listar_encuestas(request):
    if request.session.get('perfil') != 'SECPLA':
        return redirect('/login/secpla/')
    
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('/login/secpla/')
    
    try:
        usuario_activo = Usuario.objects.get(id=usuario_id)
    except Usuario.DoesNotExist:
        return redirect('/login/secpla/')
    
    encuestas = Encuesta.objects.exclude(id__isnull=True).order_by('-id')
    resumen = {
        'encuestas_vigentes': Encuesta.objects.filter(categoria='Vigente').count(),
        'encuestas_bloqueadas': Encuesta.objects.filter(categoria='Bloqueada').count(),
    }

    return render(request, 'SECPLA/listar_encuestas.html', {
        'usuario_activo': usuario_activo,
        'encuestas': encuestas,
        'resumen': resumen,
        'perfil': 'SECPLA',
    })

@require_POST
def crear_tipo_incidencia_ajax(request):
    nombre = request.POST.get('nombre_tipo', '').strip()
    direccion_id = request.POST.get('direccion_tipo')
    departamento_id = request.POST.get('departamento_tipo')

    if not nombre or not direccion_id or not departamento_id:
        return JsonResponse({'error': 'Faltan datos obligatorios'}, status=400)

    try:
        direccion = Direccion.objects.get(id=direccion_id)
        departamento = Departamento.objects.get(id=departamento_id)

        if TipoIncidencia.objects.filter(nombre_incidencia__iexact=nombre).exists():
            return JsonResponse({'error': f'Ya existe un tipo con el nombre "{nombre}".'}, status=409)

        tipo = TipoIncidencia.objects.create(
            nombre_incidencia=nombre,
            direccion=direccion,
            departamento=departamento,
            estado='Activo'
        )

        return JsonResponse({'id': tipo.id, 'nombre_incidencia': tipo.nombre})

    except Direccion.DoesNotExist:
        return JsonResponse({'error': 'Dirección no encontrada'}, status=404)
    except Departamento.DoesNotExist:
        return JsonResponse({'error': 'Departamento no encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)




