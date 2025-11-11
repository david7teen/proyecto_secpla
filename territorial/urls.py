from django.urls import path
from . import views

urlpatterns = [
    path('', views.vista_territorial, name='dashboard_territorial'),

    # CRUD de Incidencias
    path('incidencia/crear/', views.crear_incidencia, name='crear_incidencia'),
    path('incidencia/editar/<int:incidencia_id>/', views.editar_incidencia, name='editar_incidencia'),
    path('incidencia/eliminar/<int:incidencia_id>/', views.eliminar_incidencia, name='eliminar_incidencia'),
        
    # AJAX
    path('api/departamentos/<int:direccion_id>/', views.obtener_departamentos_por_direccion, name='departamentos_por_direccion'),

    # Incidencias por estado
    path('incidencias/abiertas/', views.incidencias_abiertas, name='incidencias_abiertas'),
    path('incidencias/derivadas/', views.incidencias_derivadas, name='incidencias_derivadas'),
    path('incidencias/proceso/', views.incidencias_proceso, name='incidencias_proceso'),
    path('incidencias/rechazadas/', views.incidencias_rechazadas, name='incidencias_rechazadas'),
    path('incidencias/finalizadas/', views.incidencias_finalizadas, name='incidencias_finalizadas'),
    path('incidencias/cerradas/', views.incidencias_cerradas, name='incidencias_cerradas'),
	path('ver_solicitudes/', views.ver_todas_solicitudes, name='ver_solicitudes'),
	path('incidencias/todas/', views.listar_incidencias_territorial, name='listar_incidencias_territorial'),

    # Encuestas
    #path('ver_solicitudes/', views.ver_solicitudes, name='ver_solicitudes'),
    #path('encuestas/', views.listar_encuestas, name='listar_encuestas'),
    #path('encuesta/<int:id>/ver/', views.ver_encuesta, name='ver_encuesta'),
    #path('encuesta/<int:id>/editar/', views.editar_encuesta, name='editar_encuesta'),
    #path('encuesta/<int:id>/bloquear/', views.bloquear_encuesta, name='bloquear_encuesta'),
    #path('encuesta/<int:id>/activar/', views.activar_encuesta, name='activar_encuesta'),
    path('encuestas_abiertas/', views.encuestas_abiertas, name='encuestas_abiertas'),
]
