from django.contrib.auth.models import User, Group
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
    else:
        Profile.objects.get_or_create(user=instance)
        
        
class Profile(models.Model):
    PERFIL_CHOICES = [
        ('admin', 'Usuario Administrador'),
        ('direccion', 'Usuario Dirección'),
        ('departamento', 'Usuario Departamento'),
        ('territorial', 'Usuario Territorial'),
        ('cuadrilla', 'Usuario Cuadrilla'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    perfil = models.CharField(max_length=20, choices=PERFIL_CHOICES, default='territorial')
    telefono = models.CharField(max_length=20, blank=True)
    grupo = models.ForeignKey(Group, on_delete=models.CASCADE, default=1)
    activo = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['user__username']

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_perfil_display()}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
