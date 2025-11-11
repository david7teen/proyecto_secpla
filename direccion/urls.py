from django.urls import path
from . import views

urlpatterns = [
    path('', views.vista_direccion, name='dashboard_direccion'),

    path('incidencias/pendientes/', views.incidencias_pendientes, name='dir_incidencias_pendientes'),
    path('incidencias/derivadas/', views.incidencias_derivadas, name='dir_incidencias_derivadas'),
    path('incidencias/rechazadas/', views.incidencias_rechazadas, name='dir_incidencias_rechazadas'),
    path('incidencias/finalizadas/', views.incidencias_finalizadas, name='dir_incidencias_finalizadas'),
    path('incidencia/ver/<int:incidencia_id>/', views.ver_incidencia_direccion, name='dir_ver_incidencia'),
]