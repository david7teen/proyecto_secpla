from django.contrib import admin
from django.utils import timezone
from .models import (
    Direccion, Departamento, TipoIncidencia, Encuesta, Pregunta,
    Solicitud, Cuadrilla, UsuarioCuadrilla, ArchivoAdjunto, 
    Respuesta, SeguimientoSolicitud
)

@admin.register(Direccion)
class DireccionAdmin(admin.ModelAdmin):
    list_display = ("nombre_direccion", "nombre_encargado", "correo_encargado", "state", "created")
    search_fields = ("nombre_direccion", "nombre_encargado", "correo_encargado")
    list_filter = ("state", "created")
    ordering = ("nombre_direccion",)

@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ("nombre_departamento", "direccion", "nombre_encargado", "state")
    search_fields = ("nombre_departamento", "nombre_encargado", "direccion__nombre_direccion")
    list_filter = ("direccion", "state")
    ordering = ("nombre_departamento",)

@admin.register(TipoIncidencia)
class TipoIncidenciaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "departamento", "state", "created")
    search_fields = ("nombre", "descripcion", "departamento__nombre_departamento")
    list_filter = ("departamento", "state")
    ordering = ("nombre",)

@admin.register(Encuesta)
class EncuestaAdmin(admin.ModelAdmin):
    list_display = ("titulo", "tipo_incidencia", "prioridad", "bloqueada", "state", "created")
    search_fields = ("titulo", "descripcion", "nombre_vecino")
    list_filter = ("prioridad", "bloqueada", "state", "tipo_incidencia")
    ordering = ("-created",)

@admin.register(Pregunta)
class PreguntaAdmin(admin.ModelAdmin):
    list_display = ("texto_pregunta", "encuesta", "tipo_respuesta", "orden", "state")
    search_fields = ("texto_pregunta", "encuesta__titulo")
    list_filter = ("tipo_respuesta", "state")
    ordering = ("encuesta", "orden")

@admin.register(Solicitud)
class SolicitudAdmin(admin.ModelAdmin):
    list_display = ("id", "encuesta", "territorial", "estado", "get_prioridad", "state", "created")
    list_filter = ("estado", "state", "created")
    search_fields = ("descripcion", "ubicacion", "encuesta__titulo")
    ordering = ("-created",)
    
    def get_prioridad(self, obj):
        return obj.encuesta.prioridad if obj.encuesta else '-'
    get_prioridad.short_description = 'Prioridad'
    get_prioridad.admin_order_field = 'encuesta__prioridad'

@admin.register(Cuadrilla)
class CuadrillaAdmin(admin.ModelAdmin):
    list_display = ("nombre_cuadrilla", "departamento", "state", "created")
    list_filter = ("departamento", "state")
    search_fields = ("nombre_cuadrilla", "departamento__nombre_departamento")
    ordering = ("nombre_cuadrilla",)

@admin.register(UsuarioCuadrilla)
class UsuarioCuadrillaAdmin(admin.ModelAdmin):
    list_display = ("usuario", "cuadrilla", "created")
    list_filter = ("cuadrilla", "created")
    search_fields = ("usuario__username", "cuadrilla__nombre_cuadrilla")
    ordering = ("cuadrilla", "usuario")

@admin.register(ArchivoAdjunto)
class ArchivoAdjuntoAdmin(admin.ModelAdmin):
    list_display = ("id", "solicitud", "tipo", "created")
    list_filter = ("tipo",)
    search_fields = ("solicitud__id", "descripcion")
    ordering = ("-created",)

@admin.register(Respuesta)
class RespuestaAdmin(admin.ModelAdmin):
    list_display = ("id", "solicitud", "pregunta", "created")
    search_fields = ("solicitud__id", "pregunta__texto_pregunta")
    ordering = ("-created",)

@admin.register(SeguimientoSolicitud)
class SeguimientoSolicitudAdmin(admin.ModelAdmin):
    list_display = ("id", "solicitud", "estado_anterior", "estado_nuevo", "usuario", "created")
    list_filter = ("estado_anterior", "estado_nuevo", "created")
    search_fields = ("solicitud__id", "usuario__username")
    ordering = ("-created",)
