from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from registration.models import Profile
# Importamos el nuevo modelo y formulario
from .models import Direccion, Departamento, Cuadrilla
from .forms import DireccionForm, DepartamentoForm, CuadrillaForm  

# ... (Aquí irían todas tus vistas existentes de direccion_ y departamento_) ...


# ==================================================
# VISTAS PARA CUADRILLA (NUEVAS)
# ==================================================

@login_required
def cuadrilla_listar(request):
    try:
        profile = Profile.objects.get(user_id=request.user.id)
    except Profile.DoesNotExist:
        messages.info(request, 'Hubo un error con tu perfil.')
        return redirect('login')
    
    # Verificación de perfil
    if profile.group_id != 1:
        return redirect('logout')

    # Optimizamos la consulta
    cuadrillas = Cuadrilla.objects.select_related('departamento').all().order_by('nombre')
    return render(request, 'orgs/cuadrilla_listar.html', {'cuadrillas': cuadrillas})


@login_required
def cuadrilla_crear(request):
    try:
        profile = Profile.objects.get(user_id=request.user.id)
    except Profile.DoesNotExist:
        messages.info(request, 'Hubo un error con tu perfil.')
        return redirect('login')
    
    if profile.group_id != 1:
        return redirect('logout')

    if request.method == 'POST':
        form = CuadrillaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cuadrilla creada correctamente.')
            return redirect('cuadrilla_listar')
        else:
            messages.error(request, 'Corrige los errores del formulario.')
    else:
        form = CuadrillaForm()

    return render(request, 'orgs/cuadrilla_crear.html', {'form': form})


@login_required
def cuadrilla_editar(request, cuadrilla_id):
    try:
        profile = Profile.objects.get(user_id=request.user.id)
    except Profile.DoesNotExist:
        messages.info(request, 'Hubo un error con tu perfil.')
        return redirect('login')
    
    if profile.group_id != 1:
        return redirect('logout')

    cuadrilla = get_object_or_404(Cuadrilla, pk=cuadrilla_id)

    if request.method == 'POST':
        form = CuadrillaForm(request.POST, instance=cuadrilla)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cuadrilla actualizada correctamente.')
            return redirect('cuadrilla_listar')
        else:
            messages.error(request, 'Corrige los errores del formulario.')
    else:
        form = CuadrillaForm(instance=cuadrilla)

    return render(request, 'orgs/cuadrilla_editar.html', {
        'form': form,
        'cuadrilla_data': cuadrilla # Usamos 'cuadrilla_data' para consistencia
    })


@login_required
def cuadrilla_ver(request, cuadrilla_id):
    cuadrilla = get_object_or_404(Cuadrilla, pk=cuadrilla_id)
    # Usamos 'cuadrilla_data' para consistencia
    return render(request, 'orgs/cuadrilla_ver.html', {'cuadrilla_data': cuadrilla})


@login_required
def cuadrilla_bloquear(request, cuadrilla_id):
    cuadrilla = get_object_or_404(Cuadrilla, pk=cuadrilla_id)
    if cuadrilla.estado == 'Activo':
        cuadrilla.estado = 'Inactivo'
        messages.warning(request, f'La cuadrilla "{cuadrilla.nombre}" fue bloqueada.')
    else:
        cuadrilla.estado = 'Activo'
        messages.success(request, f'La cuadrilla "{cuadrilla.nombre}" fue activada.')
    cuadrilla.save()
    return redirect('cuadrilla_listar')


@login_required
def cuadrilla_eliminar(request, cuadrilla_id):
    cuadrilla = get_object_or_404(Cuadrilla, pk=cuadrilla_id)
    try:
        cuadrilla.delete()
        messages.success(request, 'Cuadrilla eliminada correctamente.')
    except:
        # Mensaje genérico por si tiene dependencias no visibles en estos archivos
        messages.error(request, 'No se puede eliminar: puede tener dependencias.')
    return redirect('cuadrilla_listar')