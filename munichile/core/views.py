from django.shortcuts import render
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Avg, Count, Q
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseNotFound, HttpResponseRedirect)
from django.shortcuts import redirect, render
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

from registration.models import Profile

# Create your views here.
def home(request):
    return redirect('login')

@login_required
def pre_check_profile(request):
    pass

@login_required
def check_profile(request):
    try:
        # ARREGLO: Crea el perfil si no existe
        profile, created = Profile.objects.get_or_create(user_id=request.user.id)
    except Exception as e:
        messages.add_message(request, messages.INFO, f'Hubo un error con su usuario: {e}')
        return redirect('login')

    # CÓDIGO ORIGINAL (ahora funcionará gracias al Paso 3)
    if profile.group_id == 1:
        return redirect('main_admin')
    else:
        # Aquí irá la lógica para otros perfiles
        return redirect('logout')


@login_required
def main_admin(request):
    try:
        # ARREGLO: Crea el perfil si no existe
        profile, created = Profile.objects.get_or_create(user_id=request.user.id)
    except Exception as e:
        messages.add_message(request, messages.INFO, f'Hubo un error con su usuario: {e}')
        return redirect('login')
    
    # CÓDIGO ORIGINAL (ahora funcionará)
    if profile.group_id == 1:
        template_name = 'core/main_admin.html'
        return render(request,template_name)
    else:
        return redirect('logout')