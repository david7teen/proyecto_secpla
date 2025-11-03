from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.models import User
from registration.models import Profile
from .models import *
from .forms import *

@login_required
def main_gestion(request):
    return render(request, "gestion/main_gestion.html", {
        "titulo": "Gestión Municipal",
        "nota": "Sistema integral de gestión de incidencias municipales"
    })

@login_required
def usuario_list(request):
    if request.user.profile.perfil != 'admin':
        messages.error(request, 'Acceso denegado')
        return redirect('check_profile')
    
    q = request.GET.get("q", "").strip()
    usuarios = User.objects.select_related('profile').all().order_by('first_name')
    
    if q:
        usuarios = usuarios.filter(
            Q(first_name__icontains=q) | 
            Q(last_name__icontains=q) |
            Q(email__icontains=q) |
            Q(profile__telefono__icontains=q)
        )
    
    return render(request, "gestion/usuario_list.html", {"items": usuarios, "q": q})

@login_required
def usuario_create(request):
    if request.user.profile.perfil != 'admin':
        messages.error(request, 'Acceso denegado')
        return redirect('check_profile')
    
    if request.method == "POST":
        form = UsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Usuario creado correctamente.")
            return redirect("gestion_usuario_list")
        messages.error(request, "Error en el formulario.")
    else:
        form = UsuarioForm()
    return render(request, "gestion/usuario_form.html", {"form": form, "modo": "crear"})

@login_required
def usuario_update(request, pk):
    if request.user.profile.perfil != 'admin':
        messages.error(request, 'Acceso denegado')
        return redirect('check_profile')
    
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form = UsuarioEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario actualizado.")
            return redirect("gestion_usuario_list")
    else:
        form = UsuarioEditForm(instance=user)
    return render(request, "gestion/usuario_form.html", {"form": form, "modo": "editar", "obj": user})

@login_required
def usuario_toggle(request, pk):
    if request.user.profile.perfil != 'admin':
        messages.error(request, 'Acceso denegado')
        return redirect('check_profile')
    
    user = get_object_or_404(User, pk=pk)
    profile = user.profile
    profile.activo = not profile.activo
    profile.save()
    
    action = "activado" if profile.activo else "bloqueado"
    messages.success(request, f"Usuario {action} correctamente.")
    return redirect("gestion_usuario_list")

@login_required
def usuario_detail(request, pk):
    if request.user.profile.perfil != 'admin':
        messages.error(request, 'Acceso denegado')
        return redirect('check_profile')
    
    user = get_object_or_404(User, pk=pk)
    return render(request, "gestion/usuario_detail.html", {"obj": user})

def direccion_list(request):
    q = request.GET.get("q", "").strip()
    qs = Direccion.objects.all().order_by("nombre_direccion")
    if q:
        qs = qs.filter(nombre_direccion__icontains=q)
    return render(request, "gestion/direccion_list.html", {"items": qs, "q": q})

def direccion_create(request):
    if request.method == "POST":
        form = DireccionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Dirección creada correctamente.")
            return redirect("gestion_direccion_list")
        messages.error(request, "Error en el formulario.")
    else:
        form = DireccionForm()
    return render(request, "gestion/direccion_form.html", {"form": form, "modo": "crear"})

def direccion_update(request, pk):
    obj = get_object_or_404(Direccion, pk=pk)
    if request.method == "POST":
        form = DireccionForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Dirección actualizada.")
            return redirect("gestion_direccion_list")
    else:
        form = DireccionForm(instance=obj)
    return render(request, "gestion/direccion_form.html", {"form": form, "modo": "editar", "obj": obj})

def direccion_delete(request, pk):
    obj = get_object_or_404(Direccion, pk=pk)
    if request.method == "POST":
        obj.state = "Inactivo"
        obj.save()
        messages.success(request, "Dirección bloqueada.")
        return redirect("gestion_direccion_list")
    return render(request, "gestion/direccion_confirm_delete.html", {"obj": obj})

def direccion_detail(request, pk):
    obj = get_object_or_404(Direccion, pk=pk)
    departamentos = obj.departamentos.all()
    return render(request, "gestion/direccion_detail.html", {"obj": obj, "departamentos": departamentos})

def departamento_list(request):
    q = request.GET.get("q", "").strip()
    qs = Departamento.objects.select_related("direccion").order_by("nombre_departamento")
    if q:
        qs = qs.filter(
            Q(nombre_departamento__icontains=q) |
            Q(direccion__nombre_direccion__icontains=q)
        )
    return render(request, "gestion/departamento_list.html", {"items": qs, "q": q})

def departamento_create(request):
    if request.method == "POST":
        form = DepartamentoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Departamento creado correctamente.")
            return redirect("gestion_departamento_list")
        messages.error(request, "Error en el formulario.")
    else:
        form = DepartamentoForm()
    return render(request, "gestion/departamento_form.html", {"form": form, "modo": "crear"})

def departamento_update(request, pk):
    obj = get_object_or_404(Departamento, pk=pk)
    if request.method == "POST":
        form = DepartamentoForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Departamento actualizado.")
            return redirect("gestion_departamento_list")
    else:
        form = DepartamentoForm(instance=obj)
    return render(request, "gestion/departamento_form.html", {"form": form, "modo": "editar", "obj": obj})

def departamento_delete(request, pk):
    obj = get_object_or_404(Departamento, pk=pk)
    if request.method == "POST":
        obj.state = "Inactivo"
        obj.save()
        messages.success(request, "Departamento bloqueado.")
        return redirect("gestion_departamento_list")
    return render(request, "gestion/departamento_confirm_delete.html", {"obj": obj})

def departamento_detail(request, pk):
    obj = get_object_or_404(Departamento, pk=pk)
    tipos_incidencia = obj.tipos_incidencia.all()
    cuadrillas = obj.cuadrillas.all()
    return render(request, "gestion/departamento_detail.html", {
        "obj": obj, 
        "tipos_incidencia": tipos_incidencia,
        "cuadrillas": cuadrillas
    })

def tipo_list(request):
    q = request.GET.get("q", "").strip()
    qs = TipoIncidencia.objects.select_related("departamento").order_by("nombre")
    if q:
        qs = qs.filter(
            Q(nombre__icontains=q) |
            Q(departamento__nombre_departamento__icontains=q)
        )
    return render(request, "gestion/tipo_list.html", {"items": qs, "q": q})

def tipo_create(request):
    if request.method == "POST":
        form = TipoIncidenciaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Tipo de Incidencia creado correctamente.")
            return redirect("gestion_tipo_list")
        messages.error(request, "Error en el formulario.")
    else:
        form = TipoIncidenciaForm()
    return render(request, "gestion/tipo_form.html", {"form": form, "modo": "crear"})

def tipo_update(request, pk):
    obj = get_object_or_404(TipoIncidencia, pk=pk)
    if request.method == "POST":
        form = TipoIncidenciaForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Tipo de Incidencia actualizado.")
            return redirect("gestion_tipo_list")
    else:
        form = TipoIncidenciaForm(instance=obj)
    return render(request, "gestion/tipo_form.html", {"form": form, "modo": "editar", "obj": obj})

def tipo_delete(request, pk):
    obj = get_object_or_404(TipoIncidencia, pk=pk)
    if request.method == "POST":
        obj.state = "Inactivo"
        obj.save()
        messages.success(request, "Tipo de Incidencia bloqueado.")
        return redirect("gestion_tipo_list")
    return render(request, "gestion/tipo_confirm_delete.html", {"obj": obj})

def tipo_detail(request, pk):
    obj = get_object_or_404(TipoIncidencia, pk=pk)
    encuestas = obj.encuestas.all()
    return render(request, "gestion/tipo_detail.html", {"obj": obj, "encuestas": encuestas})

def cuadrilla_list(request):
    q = request.GET.get("q", "").strip()
    qs = Cuadrilla.objects.select_related("departamento").order_by("nombre_cuadrilla")
    if q:
        qs = qs.filter(
            Q(nombre_cuadrilla__icontains=q) |
            Q(departamento__nombre_departamento__icontains=q)
        )
    return render(request, "gestion/cuadrilla_list.html", {"items": qs, "q": q})

def cuadrilla_create(request):
    if request.method == "POST":
        form = CuadrillaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cuadrilla creada correctamente.")
            return redirect("gestion_cuadrilla_list")
        messages.error(request, "Error en el formulario.")
    else:
        form = CuadrillaForm()
    return render(request, "gestion/cuadrilla_form.html", {"form": form, "modo": "crear"})

def cuadrilla_update(request, pk):
    obj = get_object_or_404(Cuadrilla, pk=pk)
    if request.method == "POST":
        form = CuadrillaForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Cuadrilla actualizada.")
            return redirect("gestion_cuadrilla_list")
    else:
        form = CuadrillaForm(instance=obj)
    return render(request, "gestion/cuadrilla_form.html", {"form": form, "modo": "editar", "obj": obj})

def cuadrilla_delete(request, pk):
    obj = get_object_or_404(Cuadrilla, pk=pk)
    if request.method == "POST":
        obj.state = "Inactivo"
        obj.save()
        messages.success(request, "Cuadrilla bloqueada.")
        return redirect("gestion_cuadrilla_list")
    return render(request, "gestion/cuadrilla_confirm_delete.html", {"obj": obj})

def cuadrilla_detail(request, pk):
    obj = get_object_or_404(Cuadrilla, pk=pk)
    usuarios_cuadrilla = UsuarioCuadrilla.objects.filter(cuadrilla=obj).select_related('usuario')
    return render(request, "gestion/cuadrilla_detail.html", {
        "obj": obj,
        "usuarios_cuadrilla": usuarios_cuadrilla
    })

def encuesta_list(request):
    q = request.GET.get("q", "").strip()
    qs = Encuesta.objects.select_related("tipo_incidencia").order_by("-created")
    if q:
        qs = qs.filter(
            Q(titulo__icontains=q) |
            Q(tipo_incidencia__nombre__icontains=q)
        )
    return render(request, "gestion/encuesta_list.html", {"items": qs, "q": q})

def encuesta_create(request):
    if request.method == "POST":
        form = EncuestaForm(request.POST)
        if form.is_valid():
            encuesta = form.save()
            messages.success(request, "Encuesta creada correctamente.")
            return redirect("gestion_encuesta_list")
        messages.error(request, "Error en el formulario.")
    else:
        form = EncuestaForm()
    return render(request, "gestion/encuesta_form.html", {"form": form, "modo": "crear"})

def encuesta_update(request, pk):
    obj = get_object_or_404(Encuesta, pk=pk)
    if obj.bloqueada:
        messages.error(request, "No se puede editar una encuesta bloqueada.")
        return redirect("gestion_encuesta_list")
        
    if request.method == "POST":
        form = EncuestaForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Encuesta actualizada.")
            return redirect("gestion_encuesta_list")
    else:
        form = EncuestaForm(instance=obj)
    return render(request, "gestion/encuesta_form.html", {"form": form, "modo": "editar", "obj": obj})

def encuesta_delete(request, pk):
    obj = get_object_or_404(Encuesta, pk=pk)
    if request.method == "POST":
        obj.state = "Inactivo"
        obj.save()
        messages.success(request, "Encuesta bloqueada.")
        return redirect("gestion_encuesta_list")
    return render(request, "gestion/encuesta_confirm_delete.html", {"obj": obj})

def encuesta_toggle(request, pk):
    obj = get_object_or_404(Encuesta, pk=pk)
    obj.bloqueada = not obj.bloqueada
    obj.save()
    action = "bloqueada" if obj.bloqueada else "desbloqueada"
    messages.success(request, f"Encuesta {action}.")
    return redirect("gestion_encuesta_list")

def encuesta_detail(request, pk):
    obj = get_object_or_404(Encuesta, pk=pk)
    preguntas = obj.preguntas.all().order_by('orden')
    return render(request, "gestion/encuesta_detail.html", {
        "obj": obj, 
        "preguntas": preguntas
    })

def solicitud_list(request):
    perfil = request.user.profile.perfil
    if perfil == 'territorial':
        items = Solicitud.objects.filter(territorial=request.user)
    elif perfil == 'cuadrilla':
        cuadrillas_usuario = UsuarioCuadrilla.objects.filter(usuario=request.user).values_list('cuadrilla', flat=True)
        items = Solicitud.objects.filter(cuadrilla_asignada__in=cuadrillas_usuario)
    elif perfil == 'direccion':
        items = Solicitud.objects.filter(departamento_asignado__direccion__in=Direccion.objects.filter(
            Q(nombre_encargado=request.user.get_full_name()) | 
            Q(correo_encargado=request.user.email)
        ))
    elif perfil == 'departamento':
        items = Solicitud.objects.filter(departamento_asignado__in=Departamento.objects.filter(
            Q(nombre_encargado=request.user.get_full_name()) | 
            Q(correo_encargado=request.user.email)
        ))
    else:
        items = Solicitud.objects.all()
    
    items = items.select_related('encuesta', 'territorial').order_by('-created')
    return render(request, "gestion/solicitud_list.html", {"items": items})

def solicitud_create(request):
    if request.method == "POST":
        form = SolicitudForm(request.POST)
        if form.is_valid():
            solicitud = form.save(commit=False)
            if request.user.profile.perfil == 'territorial':
                solicitud.territorial = request.user
            solicitud.save()
            messages.success(request, "Solicitud creada correctamente.")
            return redirect("gestion_solicitud_list")
        messages.error(request, "Error en el formulario.")
    else:
        form = SolicitudForm()
    return render(request, "gestion/solicitud_form.html", {"form": form, "modo": "crear"})

def solicitud_update(request, pk):
    obj = get_object_or_404(Solicitud, pk=pk)
    if request.method == "POST":
        form = SolicitudForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Solicitud actualizada.")
            return redirect("gestion_solicitud_list")
    else:
        form = SolicitudForm(instance=obj)
    return render(request, "gestion/solicitud_form.html", {"form": form, "modo": "editar", "obj": obj})

def solicitud_delete(request, pk):
    obj = get_object_or_404(Solicitud, pk=pk)
    if request.method == "POST":
        obj.state = "Inactivo"
        obj.save()
        messages.success(request, "Solicitud bloqueada.")
        return redirect("gestion_solicitud_list")
    return render(request, "gestion/solicitud_confirm_delete.html", {"obj": obj})

def solicitud_detail(request, pk):
    obj = get_object_or_404(Solicitud, pk=pk)
    adjuntos = obj.adjuntos.all()
    seguimientos = obj.seguimientos.all()
    return render(request, "gestion/solicitud_detail.html", {
        "obj": obj,
        "adjuntos": adjuntos,
        "seguimientos": seguimientos
    })

def solicitud_derivar(request, pk):
    obj = get_object_or_404(Solicitud, pk=pk)
    if request.method == "POST":
        form = AsignarSolicitudForm(request.POST, instance=obj)
        if form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.estado = 'derivada'
            solicitud.fecha_derivacion = timezone.now()
            solicitud.save()
            
            SeguimientoSolicitud.objects.create(
                solicitud=solicitud,
                estado_anterior=obj.estado,
                estado_nuevo='derivada',
                usuario=request.user,
                comentario=f"Derivada a {solicitud.departamento_asignado}"
            )
            messages.success(request, "Solicitud derivada correctamente.")
            return redirect("gestion_solicitud_list")
    else:
        form = AsignarSolicitudForm(instance=obj)
    return render(request, "gestion/solicitud_derivar.html", {"form": form, "obj": obj})

def solicitud_asignar_cuadrilla(request, pk):
    obj = get_object_or_404(Solicitud, pk=pk)
    if request.method == "POST":
        cuadrilla_id = request.POST.get('cuadrilla_asignada')
        if cuadrilla_id:
            obj.cuadrilla_asignada_id = cuadrilla_id
            obj.estado = 'en_proceso'
            obj.fecha_asignacion_cuadrilla = timezone.now()
            obj.save()
            
            SeguimientoSolicitud.objects.create(
                solicitud=obj,
                estado_anterior=obj.estado,
                estado_nuevo='en_proceso',
                usuario=request.user,
                comentario=f"Asignada a cuadrilla {obj.cuadrilla_asignada}"
            )
            messages.success(request, "Solicitud asignada a cuadrilla.")
        return redirect("gestion_solicitud_list")
    
    cuadrillas = Cuadrilla.objects.filter(departamento=obj.departamento_asignado, state='Activo')
    return render(request, "gestion/solicitud_asignar.html", {"obj": obj, "cuadrillas": cuadrillas})

def solicitud_finalizar(request, pk):
    obj = get_object_or_404(Solicitud, pk=pk)
    if request.method == "POST":
        form = ArchivoAdjuntoForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = form.save(commit=False)
            archivo.solicitud = obj
            archivo.save()
            
            obj.estado = 'finalizada'
            obj.fecha_finalizacion = timezone.now()
            obj.save()
            
            SeguimientoSolicitud.objects.create(
                solicitud=obj,
                estado_anterior=obj.estado,
                estado_nuevo='finalizada',
                usuario=request.user,
                comentario="Solicitud finalizada por cuadrilla"
            )
            messages.success(request, "Solicitud finalizada correctamente.")
            return redirect("gestion_solicitud_list")
    else:
        form = ArchivoAdjuntoForm()
    return render(request, "gestion/solicitud_finalizar.html", {"form": form, "obj": obj})

@login_required
def solicitud_validar(request, pk):
    if request.user.profile.perfil != 'territorial':
        messages.error(request, 'Acceso denegado')
        return redirect('check_profile')
    
    obj = get_object_or_404(Solicitud, pk=pk, territorial=request.user, estado='finalizada')
    adjuntos = obj.adjuntos.all()
    
    if request.method == "POST":
        accion = request.POST.get('accion')
        comentario = request.POST.get('comentario_validacion', '')
        
        if accion == 'validar':
            obj.estado = 'validada'
            mensaje = "Solicitud validada correctamente."
        elif accion == 'rechazar':
            obj.estado = 'rechazada'
            obj.cuadrilla_asignada = None
            obj.fecha_asignacion_cuadrilla = None
            obj.fecha_finalizacion = None
            mensaje = "Validación rechazada, la solicitud vuelve a estado derivada."
        
        obj.save()
        
        SeguimientoSolicitud.objects.create(
            solicitud=obj,
            estado_anterior='finalizada',
            estado_nuevo=obj.estado,
            usuario=request.user,
            comentario=comentario
        )
        
        messages.success(request, mensaje)
        return redirect("gestion_solicitud_list")
    
    return render(request, "gestion/solicitud_validar.html", {
        "obj": obj,
        "adjuntos": adjuntos
    })

@login_required
def pregunta_create(request, encuesta_id):
    encuesta = get_object_or_404(Encuesta, pk=encuesta_id)
    
    if encuesta.bloqueada:
        messages.error(request, "No se pueden agregar preguntas a una encuesta bloqueada.")
        return redirect("gestion_encuesta_detail", pk=encuesta_id)
    
    if request.method == "POST":
        form = PreguntaForm(request.POST)
        if form.is_valid():
            pregunta = form.save(commit=False)
            pregunta.encuesta = encuesta
            pregunta.save()
            messages.success(request, "Pregunta agregada correctamente.")
            return redirect("gestion_encuesta_detail", pk=encuesta_id)
    else:
        # Calcular el siguiente orden
        ultima_pregunta = encuesta.preguntas.order_by('-orden').first()
        siguiente_orden = (ultima_pregunta.orden + 1) if ultima_pregunta else 1
        
        form = PreguntaForm(initial={'orden': siguiente_orden})
    
    return render(request, "gestion/pregunta_form.html", {
        "form": form, 
        "modo": "crear", 
        "encuesta": encuesta
    })

@login_required
def pregunta_update(request, encuesta_id, pregunta_id):
    encuesta = get_object_or_404(Encuesta, pk=encuesta_id)
    
    if encuesta.bloqueada:
        messages.error(request, "No se pueden editar preguntas de una encuesta bloqueada.")
        return redirect("gestion_encuesta_detail", pk=encuesta_id)
    
    pregunta = get_object_or_404(Pregunta, pk=pregunta_id, encuesta=encuesta)
    
    if request.method == "POST":
        form = PreguntaForm(request.POST, instance=pregunta)
        if form.is_valid():
            form.save()
            messages.success(request, "Pregunta actualizada correctamente.")
            return redirect("gestion_encuesta_detail", pk=encuesta_id)
    else:
        form = PreguntaForm(instance=pregunta)
    
    return render(request, "gestion/pregunta_form.html", {
        "form": form, 
        "modo": "editar", 
        "encuesta": encuesta,
        "obj": pregunta
    })

@login_required
def pregunta_delete(request, encuesta_id, pregunta_id):
    encuesta = get_object_or_404(Encuesta, pk=encuesta_id)
    
    if encuesta.bloqueada:
        messages.error(request, "No se pueden eliminar preguntas de una encuesta bloqueada.")
        return redirect("gestion_encuesta_detail", pk=encuesta_id)
    
    pregunta = get_object_or_404(Pregunta, pk=pregunta_id, encuesta=encuesta)
    
    if request.method == "POST":
        pregunta.delete()
        messages.success(request, "Pregunta eliminada correctamente.")
        return redirect("gestion_encuesta_detail", pk=encuesta_id)
    
    return render(request, "gestion/pregunta_confirm_delete.html", {
        "obj": pregunta,
        "encuesta": encuesta
    })

@login_required
def usuariocuadrilla_list(request):
    if request.user.profile.perfil != 'admin':
        messages.error(request, 'Acceso denegado')
        return redirect('check_profile')
    
    items = UsuarioCuadrilla.objects.select_related('usuario', 'cuadrilla__departamento').all().order_by('cuadrilla__nombre_cuadrilla')
    return render(request, "gestion/usuariocuadrilla_list.html", {"items": items})

@login_required
def usuariocuadrilla_create(request):
    if request.user.profile.perfil != 'admin':
        messages.error(request, 'Acceso denegado')
        return redirect('check_profile')
    
    if request.method == "POST":
        form = UsuarioCuadrillaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario asignado a cuadrilla correctamente.")
            return redirect("gestion_usuariocuadrilla_list")
    else:
        form = UsuarioCuadrillaForm()
    return render(request, "gestion/usuariocuadrilla_form.html", {"form": form})

@login_required
def usuariocuadrilla_delete(request, pk):
    if request.user.profile.perfil != 'admin':
        messages.error(request, 'Acceso denegado')
        return redirect('check_profile')
    
    obj = get_object_or_404(UsuarioCuadrilla, pk=pk)
    
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Asignación eliminada correctamente.")
        return redirect("gestion_usuariocuadrilla_list")
    
    return render(request, "gestion/usuariocuadrilla_confirm_delete.html", {"obj": obj})

# APIs para combos dependientes
def get_departamentos_por_direccion(request):
    direccion_id = request.GET.get('direccion_id')
    if direccion_id:
        departamentos = Departamento.objects.filter(
            direccion_id=direccion_id, state='Activo'
        ).values('id', 'nombre_departamento')
        return JsonResponse(list(departamentos), safe=False)
    return JsonResponse([], safe=False)

def get_cuadrillas_por_departamento(request):
    departamento_id = request.GET.get('departamento_id')
    if departamento_id:
        cuadrillas = Cuadrilla.objects.filter(
            departamento_id=departamento_id, state='Activo'
        ).values('id', 'nombre_cuadrilla')
        return JsonResponse(list(cuadrillas), safe=False)
    return JsonResponse([], safe=False)

def get_tipos_incidencia_por_departamento(request):
    departamento_id = request.GET.get('departamento_id')
    if departamento_id:
        tipos_incidencia = TipoIncidencia.objects.filter(
            departamento_id=departamento_id, state='Activo'
        ).values('id', 'nombre')
        return JsonResponse(list(tipos_incidencia), safe=False)
    return JsonResponse([], safe=False)
