from django.urls import path
from . import views

urlpatterns = [
    path('', views.vista_cuadrilla, name='dashboard_cuadrilla'),
    path('incidencias/activas/', views.incidencias_activas_cuadrilla, name='incidencias_activas_cuadrilla'),
    path('incidencias/responder/<int:incidencia_id>/', views.responder_incidencia, name='responder_incidencia'),
    path('incidencias/', views.listado_incidencias_cuadrilla, name='listado_incidencias_cuadrilla'),
    path('incidencias/tomar/<int:incidencia_id>/', views.tomar_incidencia, name='tomar_incidencia'),
    path('incidencias/rechazar/<int:incidencia_id>/', views.rechazar_incidencia, name='rechazar_incidencia'),
    path('incidencias/proceso/', views.incidencias_proceso, name='incidencias_proceso'),
    path('incidencias/finalizadas/', views.incidencias_finalizadas_cuadrilla, name='incidencias_finalizadas_cuadrilla'),
    path('reporte/trabajo/', views.reporte_trabajo, name='reporte_trabajo'),
]
