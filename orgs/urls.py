from django.urls import path
from . import views

urlpatterns = [
    # (Se eliminaron las URLs de 'direcciones' y 'departamentos')

    # ---------- URLs de Cuadrilla (NUEVAS) ----------
    path('cuadrillas/', views.cuadrilla_listar, name='cuadrilla_listar'),
    path('cuadrillas/crear/', views.cuadrilla_crear, name='cuadrilla_crear'),
    path('cuadrillas/editar/<int:cuadrilla_id>/', views.cuadrilla_editar, name='cuadrilla_editar'),
    path('cuadrillas/ver/<int:cuadrilla_id>/', views.cuadrilla_ver, name='cuadrilla_ver'),
    path('cuadrillas/bloquear/<int:cuadrilla_id>/', views.cuadrilla_bloquear, name='cuadrilla_bloquear'),
    path('cuadrillas/eliminar/<int:cuadrilla_id>/', views.cuadrilla_eliminar, name='cuadrilla_eliminar'),
]