from django.db import models
from departamento.models import Departamento
from direccion.models import Direccion
class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField()  # ← solo una vez
    telefono = models.CharField(max_length=20)
    perfil = models.CharField(max_length=50, choices=[
        ('SECPLA', 'SECPLA'),
        ('Dirección', 'Dirección'),
        ('Departamento', 'Departamento'),
        ('Territorial', 'Territorial'),
        ('Cuadrilla', 'Cuadrilla'),
    ])
    contraseña = models.CharField(max_length=100)
    estado = models.CharField(max_length=20, default='Activo')
    direccion_asociada = models.ForeignKey(
        Direccion, 
        on_delete=models.SET_NULL,  # Si se borra la dirección, el usuario no se borra
        null=True, 
        blank=True
    )
    departamento_asociado = models.ForeignKey(
    Departamento,
    on_delete=models.SET_NULL,  # Si se borra el depto, no se borra el usuario
    null=True,
    blank=True,
    related_name="usuarios_asociados")

class RecuperacionIntento(models.Model):
    correo = models.EmailField()
    perfil = models.CharField(max_length=50)
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, default='Pendiente')  # Opciones: Pendiente, Revisado, Resuelto
    observacion = models.TextField(blank=True)

    def __str__(self):
        return f"{self.correo} ({self.perfil}) - {self.estado}"

