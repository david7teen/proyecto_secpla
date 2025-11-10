from django.urls import path
from . import views

urlpatterns = [
    path('incidencias/pendientes/', views.ver_pendientes_departamento, name='ver_pendientes_departamento'),
    path('incidencias/derivadas/', views.ver_derivadas_departamento, name='ver_derivadas_departamento'),
    path('incidencias/rechazadas/', views.ver_rechazadas_departamento, name='ver_rechazadas_departamento'),
    path('incidencias/finalizadas/', views.ver_finalizadas_departamento, name='ver_finalizadas_departamento'),
	path('reporte/finalizadas/', views.reporte_finalizadas, name='reporte_finalizadas'),

    # Definen las URLs para las acciones que creamos en views.py
    path('incidencia/derivar/<int:incidencia_id>/', views.derivar_incidencia, name='derivar_incidencia'),
    path('incidencia/rechazar/<int:incidencia_id>/', views.rechazar_incidencia, name='rechazar_incidencia'),

]