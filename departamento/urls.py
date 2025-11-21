from django.urls import path
from . import views

urlpatterns = [
    path('incidencias/pendientes/', views.ver_pendientes_departamento, name='ver_pendientes_departamento'),
    path('incidencias/derivadas/', views.ver_derivadas_departamento, name='ver_derivadas_departamento'),
    path('incidencias/rechazadas/', views.ver_rechazadas_departamento, name='ver_rechazadas_departamento'),
    path('incidencias/finalizadas/', views.ver_finalizadas_departamento, name='ver_finalizadas_departamento'),
	path('reporte/finalizadas/', views.reporte_finalizadas, name='reporte_finalizadas'),

    path('incidencia/derivar/<int:incidencia_id>/', views.derivar_incidencia, name='derivar_incidencia'),
    path('incidencia/rechazar/<int:incidencia_id>/', views.rechazar_incidencia, name='rechazar_incidencia'),

    path('incidencia/ver/<int:incidencia_id>/', views.ver_incidencia_departamento, name='ver_incidencia_departamento'),
    path('incidencia/reabrir/<int:incidencia_id>/', views.reabrir_incidencia, name='reabrir_incidencia'),
    path('incidencia/editar/<int:incidencia_id>/', views.editar_incidencia_departamento, name='editar_incidencia_departamento'),
    
    path('incidencias/listar/', views.listar_incidencias_departamento, name='dep_listar_incidencias'),
]
