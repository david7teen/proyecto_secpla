from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render
from registration.models import Profile
from .forms import EncuestaForm

@login_required
def main_usuario(request):
    try:
        profile = Profile.objects.filter(user_id=request.user.id).get()
    except:
        messages.add_message(request, messages.INFO, 'Hubo un error')
        return redirect('login')
    
    if profile.group_id == 1:
        template_name = 'gestion/main_usuario.html'
        return render(request, template_name)
    else:
        return redirect('logout')
    
@login_required
def crear_encuesta(request):
    try:
        profile = Profile.objects.get(user_id=request.user.id)
    except Profile.DoesNotExist:
        messages.error(request, 'Hubo un error con su perfil.')
        return redirect('login')

    # Según requerimientos, SECPLA puede crear todo. 
    # Aquí podrías añadir 'or profile.group_id == ID_TERRITORIAL'
    if profile.group_id != 1:
        messages.error(request, 'No tiene permisos para acceder a esta sección.')
        return redirect('logout')
    
    if request.method == 'POST':
        # ¡¡IMPORTANTE: Usar request.FILES para los archivos!!
        form = EncuestaForm(request.POST, request.FILES)
        
        if form.is_valid():
            encuesta = form.save(commit=False)
            encuesta.creado_por = request.user  # Asigna el usuario logueado
            encuesta.estado = 'abierta'         # Estado inicial 
            encuesta.save()
            
            messages.success(request, '¡Incidencia (Encuesta) creada con éxito!')
            return redirect('main_admin') # O a una lista de incidencias
    else:
        form = EncuestaForm()

    template_name = 'gestion/encuesta.html'
    context = {'form': form}
    return render(request, template_name, context)