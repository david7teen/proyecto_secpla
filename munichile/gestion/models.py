from django.db import models

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

