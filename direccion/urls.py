from django.urls import path
from . import views

urlpatterns = [
    path('', views.vista_direccion, name='dashboard_direccion'),

    path('incidencias/pendientes/', views.incidencias_pendientes, name='dir_incidencias_pendientes'),
    path('incidencias/derivadas/', views.incidencias_derivadas, name='dir_incidencias_derivadas'),
    path('incidencias/rechazadas/', views.incidencias_rechazadas, name='dir_incidencias_rechazadas'),
    path('incidencias/finalizadas/', views.incidencias_finalizadas, name='dir_incidencias_finalizadas'),
    path('incidencia/ver/<int:incidencia_id>/', views.ver_incidencia_direccion, name='dir_ver_incidencia'),
    path('incidencia/rechazar/<int:incidencia_id>/', views.rechazar_incidencia_direccion, name='dir_rechazar_incidencia'),
    path('incidencia/editar/<int:incidencia_id>/', views.editar_incidencia_direccion, name='dir_editar_incidencia'),
    path('incidencia/derivar/<int:incidencia_id>/', views.derivar_incidencia_direccion, name='dir_derivar_incidencia'),
	path('incidencias/todas/', views.listar_todas_incidencias, name='dir_incidencias_todas'),
	path('incidencias/listar/', views.listar_incidencias_direccion, name='dir_listar_incidencias'),
]
