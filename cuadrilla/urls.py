from django.urls import path
from . import views

urlpatterns = [
    path('', views.vista_cuadrilla, name='dashboard_cuadrilla'),
    path('incidencias/pendientes/', views.listar_incidencias_cuadrilla, name='cuadrilla_incidencias_pendientes'),
    path('incidencias/responder/<int:incidencia_id>/', views.responder_incidencia, name='cuadrilla_responder_incidencia'),
    path('incidencias/rechazar/<int:incidencia_id>/', views.rechazar_incidencia, name='cuadrilla_rechazar_incidencia'),
    path('incidencias/tomar/<int:incidencia_id>/', views.tomar_incidencia, name='cuadrilla_tomar_incidencia'),
    path('incidencias/en-proceso/', views.incidencias_en_proceso, name='cuadrilla_incidencias_proceso'),
    path('incidencias/finalizadas/', views.incidencias_finalizadas, name='cuadrilla_incidencias_finalizadas'),
]