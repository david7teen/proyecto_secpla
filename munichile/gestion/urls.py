from django.urls import path
from . import views

urlpatterns = [
    path('main/', views.main_gestion, name='gestion_main'),
    
    # Usuarios
    path('usuario/', views.usuario_list, name='gestion_usuario_list'),
    path('usuario/nuevo/', views.usuario_create, name='gestion_usuario_create'),
    path('usuario/<int:pk>/editar/', views.usuario_update, name='gestion_usuario_update'),
    path('usuario/<int:pk>/toggle/', views.usuario_toggle, name='gestion_usuario_toggle'),
    path('usuario/<int:pk>/', views.usuario_detail, name='gestion_usuario_detail'),
    
    # Direcciones
    path('direccion/', views.direccion_list, name='gestion_direccion_list'),
    path('direccion/nuevo/', views.direccion_create, name='gestion_direccion_create'),
    path('direccion/<int:pk>/editar/', views.direccion_update, name='gestion_direccion_update'),
    path('direccion/<int:pk>/eliminar/', views.direccion_delete, name='gestion_direccion_delete'),
    path('direccion/<int:pk>/', views.direccion_detail, name='gestion_direccion_detail'),
    
    # Departamentos
    path('departamento/', views.departamento_list, name='gestion_departamento_list'),
    path('departamento/nuevo/', views.departamento_create, name='gestion_departamento_create'),
    path('departamento/<int:pk>/editar/', views.departamento_update, name='gestion_departamento_update'),
    path('departamento/<int:pk>/eliminar/', views.departamento_delete, name='gestion_departamento_delete'),
    path('departamento/<int:pk>/', views.departamento_detail, name='gestion_departamento_detail'),
    
    # Tipos de Incidencia (ÚNICAS)
    path('tipo/', views.tipo_list, name='gestion_tipo_list'),
    path('tipo/nuevo/', views.tipo_create, name='gestion_tipo_create'),
    path('tipo/<int:pk>/editar/', views.tipo_update, name='gestion_tipo_update'),
    path('tipo/<int:pk>/eliminar/', views.tipo_delete, name='gestion_tipo_delete'),
    path('tipo/<int:pk>/', views.tipo_detail, name='gestion_tipo_detail'),
    
    # Cuadrillas
    path('cuadrilla/', views.cuadrilla_list, name='gestion_cuadrilla_list'),
    path('cuadrilla/nuevo/', views.cuadrilla_create, name='gestion_cuadrilla_create'),
    path('cuadrilla/<int:pk>/editar/', views.cuadrilla_update, name='gestion_cuadrilla_update'),
    path('cuadrilla/<int:pk>/eliminar/', views.cuadrilla_delete, name='gestion_cuadrilla_delete'),
    path('cuadrilla/<int:pk>/', views.cuadrilla_detail, name='gestion_cuadrilla_detail'),
    
    # Encuestas
    path('encuesta/', views.encuesta_list, name='gestion_encuesta_list'),
    path('encuesta/nuevo/', views.encuesta_create, name='gestion_encuesta_create'),
    path('encuesta/<int:pk>/editar/', views.encuesta_update, name='gestion_encuesta_update'),
    path('encuesta/<int:pk>/eliminar/', views.encuesta_delete, name='gestion_encuesta_delete'),
    path('encuesta/<int:pk>/toggle/', views.encuesta_toggle, name='gestion_encuesta_toggle'),
    path('encuesta/<int:pk>/', views.encuesta_detail, name='gestion_encuesta_detail'),
    
    # Solicitudes
    path('solicitud/', views.solicitud_list, name='gestion_solicitud_list'),
    path('solicitud/nuevo/', views.solicitud_create, name='gestion_solicitud_create'),
    path('solicitud/<int:pk>/editar/', views.solicitud_update, name='gestion_solicitud_update'),
    path('solicitud/<int:pk>/eliminar/', views.solicitud_delete, name='gestion_solicitud_delete'),
    path('solicitud/<int:pk>/', views.solicitud_detail, name='gestion_solicitud_detail'),
    path('solicitud/<int:pk>/derivar/', views.solicitud_derivar, name='gestion_solicitud_derivar'),
    path('solicitud/<int:pk>/asignar/', views.solicitud_asignar_cuadrilla, name='gestion_solicitud_asignar'),
    path('solicitud/<int:pk>/finalizar/', views.solicitud_finalizar, name='gestion_solicitud_finalizar'),
    path('solicitud/<int:pk>/validar/', views.solicitud_validar, name='gestion_solicitud_validar'),
    
    # Preguntas en Encuestas
    path('encuesta/<int:encuesta_id>/pregunta/nueva/', views.pregunta_create, name='gestion_pregunta_create'),
    path('encuesta/<int:encuesta_id>/pregunta/<int:pregunta_id>/editar/', views.pregunta_update, name='gestion_pregunta_update'),
    path('encuesta/<int:encuesta_id>/pregunta/<int:pregunta_id>/eliminar/', views.pregunta_delete, name='gestion_pregunta_delete'),

    # Usuarios en Cuadrillas
    path('usuariocuadrilla/', views.usuariocuadrilla_list, name='gestion_usuariocuadrilla_list'),
    path('usuariocuadrilla/nuevo/', views.usuariocuadrilla_create, name='gestion_usuariocuadrilla_create'),
    path('usuariocuadrilla/<int:pk>/eliminar/', views.usuariocuadrilla_delete, name='gestion_usuariocuadrilla_delete'),
    
    # APIs para combos dependientes
    path('api/departamentos-por-direccion/', views.get_departamentos_por_direccion, name='api_departamentos_por_direccion'),
    path('api/cuadrillas-por-departamento/', views.get_cuadrillas_por_departamento, name='api_cuadrillas_por_departamento'),
    path('api/tipos-incidencia-por-departamento/', views.get_tipos_incidencia_por_departamento, name='api_tipos_incidencia_por_departamento'),
]
