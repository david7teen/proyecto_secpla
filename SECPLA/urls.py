from django.urls import path
from . import views
from .views import obtener_departamentos_por_direccion, crear_pregunta_ajax
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/<str:perfil>/', views.login_por_perfil, name='login_por_perfil'),
    path('perfil/secpla/', views.vista_secpla, name='vista_secpla'),
    path('perfil/direccion/', views.vista_direccion, name='vista_direccion'),
    path('perfil/departamento/', views.vista_departamento, name='vista_departamento'),
    path('perfil/territorial/', views.vista_territorial, name='vista_territorial'),
    path('perfil/cuadrilla/', views.vista_cuadrilla, name='vista_cuadrilla'),
    path('dashboard/', views.dashboard_secpla, name='dashboard_secpla'),

    path('crear_usuario/', views.crear_usuario, name='crear_usuario'),
    path('ver_usuario/', views.ver_usuario, name='ver_usuario'),
    path('ver_usuario_2/<int:usuario_id>/', views.ver_usuario_2, name='ver_usuario_2'),
    path('editar_usuario/<int:usuario_id>/', views.editar_usuario, name='editar_usuario'),
    path('bloquear_usuario/<int:usuario_id>/', views.bloquear_usuario, name='bloquear_usuario'),
    path('activar_usuario/<int:usuario_id>/', views.activar_usuario, name='activar_usuario'),
    path('eliminar_usuario/<int:usuario_id>/', views.eliminar_usuario, name='eliminar_usuario'),

    path('secpla/crear_direccion/', views.crear_direccion, name='crear_direccion'),
    path('ver_direccion/<int:id>/', views.ver_direccion, name='ver_direccion'),
    path('editar_direccion/<int:id>/', views.editar_direccion, name='editar_direccion'),
    path('bloquear_direccion/<int:id>/', views.bloquear_direccion, name='bloquear_direccion'),
    path('activar_direccion/<int:id>/', views.activar_direccion, name='activar_direccion'),
    path('listar_direcciones/', views.listar_direcciones, name='listar_direcciones'),

    path('secpla/crear_departamento/', views.crear_departamento, name='crear_departamento'),
    path('ver_departamento/<int:id>/', views.ver_departamento, name='ver_departamento'),
    path('editar_departamento/<int:id>/', views.editar_departamento, name='editar_departamento'),
    path('bloquear_departamento/<int:id>/', views.bloquear_departamento, name='bloquear_departamento'),
    path('activar_departamento/<int:id>/', views.activar_departamento, name='activar_departamento'),
    path('listar_departamentos/', views.listar_departamentos, name='listar_departamentos'),

    path('cuadrillas/listar/', views.listar_cuadrillas, name='listar_cuadrillas'),

    path('tipos-incidencia/crear/', views.crear_tipo_incidencia, name='crear_tipo_incidencia'),
    path('tipos-incidencia/listar/', views.listar_tipos_incidencia, name='listar_tipos_incidencia'),
    path('tipos-incidencia/editar/<int:id>/', views.editar_tipo_incidencia, name='editar_tipo_incidencia'),
    path('tipos-incidencia/eliminar/<int:id>/', views.eliminar_tipo_incidencia, name='eliminar_tipo_incidencia'),

    path('listar_incidencias/', views.listar_incidencias, name='listar_incidencias'),
    path('incidencia/actualizar-estado/<int:incidencia_id>/', views.actualizar_estado_incidencia, name='actualizar_estado_incidencia'),
    path('ver_incidencia/<int:incidencia_id>/', views.ver_incidencia, name='ver_incidencia'),

    path('secpla/crear_encuesta/', views.crear_encuesta, name='crear_encuesta'),
    path('listar_encuestas/', views.listar_encuestas, name='listar_encuestas'),
    path('ver_encuesta/<int:encuesta_id>/', views.ver_encuesta, name='ver_encuesta'),
    path('editar_encuesta/<int:encuesta_id>/', views.editar_encuesta, name='editar_encuesta'),
    path('bloquear_encuesta/<int:encuesta_id>/', views.bloquear_encuesta, name='bloquear_encuesta'),
    path('activar_encuesta/<int:encuesta_id>/', views.activar_encuesta, name='activar_encuesta'),
	path('encuesta/eliminar/<int:encuesta_id>/', views.eliminar_encuesta, name='eliminar_encuesta'),

    path('ajax/crear_pregunta/', crear_pregunta_ajax, name='crear_pregunta_ajax'),
    path('secpla/crear_pregunta_ajax/', views.crear_pregunta_ajax, name='crear_pregunta_ajax'),
    path('secpla/crear_pregunta_desde_encuesta/', views.crear_pregunta_desde_encuesta, name='crear_pregunta_desde_encuesta'),

    path('recuperar_cuenta/', views.recuperar_cuenta, name='recuperar_cuenta'),
    path('ver_intentos_recuperacion/', views.ver_intentos_recuperacion, name='ver_intentos_recuperacion'),
    path('cambiar_contraseña/<int:usuario_id>/', views.cambiar_contraseña, name='cambiar_contraseña'),

    path('api/departamentos_por_direccion/<int:direccion_id>/', views.obtener_departamentos_por_direccion, name='api_departamentos_por_direccion'),
    
    path('logout/secpla/', views.salir_secpla, name='salir_secpla'),
    
    path('recuperacion/aprobar/<int:intento_id>/', views.aprobar_recuperacion, name='aprobar_recuperacion'),
    path('recuperacion/rechazar/<int:intento_id>/', views.rechazar_recuperacion, name='rechazar_recuperacion'),
    path('recuperacion/restablecer/<int:intento_id>/', views.cambiar_contraseña_desde_recuperacion, name='cambiar_contraseña_desde_recuperacion'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
