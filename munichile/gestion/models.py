from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Q

# Constantes/choices reutilizables
ESTADOS = (("Activo", "Activo"), ("Inactivo", "Inactivo"))
PRIORIDADES = (('alta', 'Alta'), ('normal', 'Normal'), ('baja', 'Baja'))
ESTADOS_SOLICITUD = (
    ('creada', 'Creada por Territorial'),
    ('derivada', 'Derivada a Departamento'), 
    ('en_proceso', 'En Proceso por Cuadrilla'),
    ('finalizada', 'Finalizada por Cuadrilla'),
    ('validada', 'Validada por Territorial'),
    ('rechazada', 'Rechazada por Territorial'),
)
TIPOS_ARCHIVO = (('imagen', 'Imagen'), ('video', 'Video'), ('audio', 'Audio'), ('documento', 'Documento'))

class Direccion(models.Model):
    nombre_direccion = models.CharField(max_length=150, unique=True, db_index=True)
    nombre_encargado = models.CharField(max_length=120, blank=True)
    correo_encargado = models.EmailField(blank=True)
    state = models.CharField(max_length=10, choices=ESTADOS, default="Activo")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["nombre_direccion"]
        verbose_name = "Dirección"
        verbose_name_plural = "Direcciones"

    def __str__(self):
        return self.nombre_direccion

class Departamento(models.Model):
    direccion = models.ForeignKey(Direccion, on_delete=models.PROTECT, related_name="departamentos")
    nombre_departamento = models.CharField(max_length=150, db_index=True)
    nombre_encargado = models.CharField(max_length=120, blank=True)
    correo_encargado = models.EmailField(blank=True)
    state = models.CharField(max_length=10, choices=ESTADOS, default="Activo")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("direccion", "nombre_departamento")
        ordering = ["nombre_departamento"]
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"

    def __str__(self):
        return f"{self.nombre_departamento} ({self.direccion})"

class Cuadrilla(models.Model):
    nombre_cuadrilla = models.CharField(max_length=150, db_index=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.PROTECT, related_name="cuadrillas")
    state = models.CharField(max_length=10, choices=ESTADOS, default="Activo")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["nombre_cuadrilla"]
        verbose_name = "Cuadrilla"
        verbose_name_plural = "Cuadrillas"

    def __str__(self):
        return self.nombre_cuadrilla

class UsuarioCuadrilla(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    cuadrilla = models.ForeignKey(Cuadrilla, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('usuario', 'cuadrilla')
        verbose_name = "Usuario en Cuadrilla"
        verbose_name_plural = "Usuarios en Cuadrillas"

    def __str__(self):
        return f"{self.usuario.username} - {self.cuadrilla.nombre_cuadrilla}"

class TipoIncidencia(models.Model):
    departamento = models.ForeignKey(Departamento, on_delete=models.PROTECT, related_name="tipos_incidencia")
    nombre = models.CharField(max_length=150, db_index=True)
    descripcion = models.TextField(blank=True)
    state = models.CharField(max_length=10, choices=ESTADOS, default="Activo")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("departamento", "nombre")
        ordering = ["nombre"]
        verbose_name = "Tipo de Incidencia"
        verbose_name_plural = "Tipos de Incidencia"

    def __str__(self):
        return self.nombre

class Encuesta(models.Model):
    titulo = models.CharField(max_length=200, db_index=True)
    descripcion = models.TextField(blank=True)
    ubicacion = models.CharField(max_length=200, blank=True)
    prioridad = models.CharField(max_length=10, choices=PRIORIDADES, default='normal')
    bloqueada = models.BooleanField(default=False)

    # Datos del vecino
    nombre_vecino = models.CharField(max_length=120, blank=True)
    celular_vecino = models.CharField(max_length=30, blank=True)
    correo_vecino = models.EmailField(blank=True)
    direccion_vecino = models.CharField(max_length=200, blank=True)

    tipo_incidencia = models.ForeignKey(TipoIncidencia, on_delete=models.PROTECT, related_name="encuestas")
    state = models.CharField(max_length=10, choices=ESTADOS, default="Activo")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created"]
        verbose_name = "Encuesta"
        verbose_name_plural = "Encuestas"

    def __str__(self):
        return self.titulo

class Pregunta(models.Model):
    TIPOS_RESPUESTA = (
        ('texto', 'Texto'), ('numero', 'Número'), 
        ('fecha', 'Fecha'), ('opciones', 'Opciones Múltiples')
    )
    
    encuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE, related_name="preguntas")
    texto_pregunta = models.TextField()
    tipo_respuesta = models.CharField(max_length=20, choices=TIPOS_RESPUESTA, default='texto')
    orden = models.IntegerField(default=0)
    opciones = models.TextField(blank=True, help_text="Opciones separadas por coma")
    state = models.CharField(max_length=10, choices=ESTADOS, default="Activo")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["orden", "created"]
        verbose_name = "Pregunta"
        verbose_name_plural = "Preguntas"

    def __str__(self):
        return f"{self.encuesta.titulo} - {self.texto_pregunta[:50]}"

class Solicitud(models.Model):
    encuesta = models.ForeignKey(Encuesta, on_delete=models.PROTECT, related_name="solicitudes")
    descripcion = models.TextField(blank=True)
    ubicacion = models.CharField(max_length=200, blank=True)
    comuna = models.CharField(max_length=100, blank=True, db_index=True)
    estado = models.CharField(max_length=20, choices=ESTADOS_SOLICITUD, default='creada')
    prioridad = models.CharField(max_length=10, choices=PRIORIDADES, default='normal')
    prioridad_directa = models.CharField(max_length=10, choices=PRIORIDADES, default='normal')
    
    territorial = models.ForeignKey(
        User, on_delete=models.PROTECT, 
        related_name='solicitudes_creadas',
        null=True, blank=True
    )
    departamento_asignado = models.ForeignKey(
        Departamento, on_delete=models.PROTECT, null=True, blank=True,
        related_name='solicitudes_asignadas'
    )
    cuadrilla_asignada = models.ForeignKey(
        Cuadrilla, on_delete=models.PROTECT, null=True, blank=True,
        related_name='solicitudes_asignadas'
    )
    
    # Fechas de seguimiento
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_derivacion = models.DateTimeField(null=True, blank=True)
    fecha_asignacion = models.DateTimeField(null=True, blank=True)
    fecha_finalizacion = models.DateTimeField(null=True, blank=True)
    fecha_validacion = models.DateTimeField(null=True, blank=True)
    fecha_asignacion_cuadrilla = models.DateTimeField(null=True, blank=True)
    
    usuario_valida = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, 
        related_name='solicitudes_validadas'
    )
    
    state = models.CharField(max_length=10, choices=ESTADOS, default="Activo")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-created"]
        verbose_name = "Solicitud"
        verbose_name_plural = "Solicitudes"

    def __str__(self):
        return f"Solicitud {self.id} - {self.estado}"

    def save(self, *args, **kwargs):
        # Lógica automática de fechas
        if self.estado == 'derivada' and not self.fecha_derivacion:
            self.fecha_derivacion = timezone.now()
        elif self.estado == 'en_proceso' and not self.fecha_asignacion_cuadrilla:
            self.fecha_asignacion_cuadrilla = timezone.now()
        elif self.estado == 'finalizada' and not self.fecha_finalizacion:
            self.fecha_finalizacion = timezone.now()
        elif self.estado == 'validada' and not self.fecha_validacion:
            self.fecha_validacion = timezone.now()
            
        super().save(*args, **kwargs)

class Respuesta(models.Model):
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE, related_name="respuestas")
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    valor_respuesta = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('solicitud', 'pregunta')
        verbose_name = "Respuesta"
        verbose_name_plural = "Respuestas"

    def __str__(self):
        return f"Respuesta {self.id}"

class ArchivoAdjunto(models.Model):
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE, related_name="adjuntos")
    tipo = models.CharField(max_length=20, choices=TIPOS_ARCHIVO)
    ruta_archivo = models.FileField(upload_to='adjuntos/%Y/%m/%d/')
    descripcion = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]
        verbose_name = "Archivo adjunto"
        verbose_name_plural = "Archivos adjuntos"

    def __str__(self):
        return f"Adjunto {self.id} ({self.tipo})"

class SeguimientoSolicitud(models.Model):
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE, related_name="seguimientos")
    estado_anterior = models.CharField(max_length=20, choices=ESTADOS_SOLICITUD)
    estado_nuevo = models.CharField(max_length=20, choices=ESTADOS_SOLICITUD)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    comentario = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]
        verbose_name = "Seguimiento de Solicitud"
        verbose_name_plural = "Seguimientos de Solicitudes"

    def __str__(self):
        return f"Seguimiento {self.id} - {self.estado_anterior} → {self.estado_nuevo}"
