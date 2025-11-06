from django.db import models
from django.conf import settings # Importa settings para referenciar al User

#usuario--------------------------------------------------------
class Usuario(models.Model):
    nombre = models.CharField(max_length=100, null=False, blank=False)
    apellido = models.CharField(max_length=100, null=False, blank=False)
    correo = models.EmailField(max_length=254, null=False, blank=False)
    telefono = models.CharField(max_length=20, null=False, blank=False)
    state = models.CharField(max_length=100, null=True, blank=True, default='Activo')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    PERFILES = [
        ('SECPLA', 'SECPLA'),
        ('DIRECCION', 'Dirección'),
        ('DEPARTAMENTO', 'Departamento'),
        ('TERRITORIAL', 'Territorial'),
        ('CUADRILLA', 'Cuadrilla'),
    ]
    perfil = models.CharField(max_length=240, choices=PERFILES, null=False, blank=False)


    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-created'] #por orden de creacion

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.perfil})"



#direccion--------------------------------------------------------
class Direccion(models.Model):
    nombre_direccion = models.CharField(max_length=200, null=False, blank=False)

    class Meta:
        verbose_name = 'direccion'
        verbose_name_plural = 'Direcciones'
        ordering = ['nombre_direccion']


    def __str__(self):
        return self.nombre_direccion



#departamento--------------------------------------------------------
class Departamento(models.Model):
    nombre_departamento = models.CharField(max_length=200, null=False, blank=False)
    direccion = models.ForeignKey(Direccion, on_delete=models.CASCADE, related_name='departamentos')
    
    class Meta:
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'
        ordering = ['nombre_departamento']


    def __str__(self):
        return self.nombre_departamento



#tipo_incidencia--------------------------------------------------------
class TipoIncidencia(models.Model):
    nombre = models.CharField(max_length=200, null=False, blank=False)
    descripcion = models.TextField(null=True, blank=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name='tipo_incidencias')
    
    class Meta:
        verbose_name = 'tipo_incidencia'
        verbose_name_plural = 'tipo_incidencias'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Encuesta(models.Model):
    # Definimos las opciones para Prioridad y Estado
    PRIORIDAD_CHOICES = [
        ('alta', 'Alta'),
        ('normal', 'Normal'),
        ('baja', 'Baja'),
    ]
    
    ESTADO_CHOICES = [
        ('abierta', 'Abierta'),
        ('derivada', 'Derivada'),
        ('rechazada', 'Rechazada'),
        ('finalizada', 'Finalizada'),
    ]

    # Atributos de la encuesta 
    titulo_encuesta = models.CharField(max_length=200, verbose_name="Título o nombre encuesta") # 
    descripcion = models.TextField(verbose_name="Descripción del incidente") # 
    ubicacion = models.CharField(max_length=255, verbose_name="Ubicación") # 
    
    # Archivos multimedia. 'upload_to' los guardará en una carpeta 'media/'
    imagen = models.ImageField(upload_to='encuestas/imagenes/', blank=True, null=True, verbose_name="Imagen") # 
    video = models.FileField(upload_to='encuestas/videos/', blank=True, null=True, verbose_name="Video") # 
    audio = models.FileField(upload_to='encuestas/audios/', blank=True, null=True, verbose_name="Audio") # 
    
    prioridad = models.CharField(max_length=10, choices=PRIORIDAD_CHOICES, default='normal', verbose_name="Prioridad") # 

    # Datos del vecino 
    nombre_vecino = models.CharField(max_length=100, blank=True, null=True, verbose_name="Nombre del Vecino")
    celular_vecino = models.CharField(max_length=20, blank=True, null=True, verbose_name="Celular del Vecino")
    email_vecino = models.EmailField(blank=True, null=True, verbose_name="Email del Vecino")

    # Relación con Tipo de Incidencia (el "combo") 
    tipo_incidencia = models.ForeignKey(
        TipoIncidencia, 
        on_delete=models.SET_NULL, 
        null=True, 
        verbose_name="Tipo de Incidencia"
    )
    
    # Datos de gestión interna
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='encuestas_creadas'
    )
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='abierta', verbose_name="Estado") # 
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Encuesta (Solicitud)'
        verbose_name_plural = 'Encuestas (Solicitudes)'
        ordering = ['-created']

    def __str__(self):
        return self.titulo_encuesta