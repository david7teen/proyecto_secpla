import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'muni.settings')
django.setup()

from django.contrib.auth.models import User
from registration.models import Profile

def crear_usuarios():
    usuarios = [
        {
            'username': 'secpla01',
            'email': 'secpla01@munichile.cl',
            'password': 'secpla123',
            'first_name': 'Patricio',
            'last_name': 'Jaramillo',
            'telefono': '+56912345678',
            'perfil': 'admin'
        },
        {
            'username': 'direccion01',
            'email': 'direccion01@munichile.cl',
            'password': 'direccion123',
            'first_name': 'Dovaqin',
            'last_name': 'Miranda',
            'telefono': '+56987654321',
            'perfil': 'direccion'
        },
        {
            'username': 'territorial01',
            'email': 'territorial01@munichile.cl',
            'password': 'territorial123',
            'first_name': 'Maximiliano',
            'last_name': 'Momero',
            'telefono': '+56911223344',
            'perfil': 'territorial'
        },
        {
            'username': 'cuadrilla01',
            'email': 'cuadrilla01@munichile.cl',
            'password': 'cuadrilla123',
            'first_name': 'Pedro',
            'last_name': 'Pfend',
            'telefono': '+56955667788',
            'perfil': 'cuadrilla'
        },
        {
            'username': 'departamento01',
            'email': 'departamento01@munichile.cl',
            'password': 'departamento123',
            'first_name': 'Juan',
            'last_name': 'Pfend',
            'telefono': '+56952667788',
            'perfil': 'departamento'
        }
    ]
    
    for datos in usuarios:
        try:
            user = User.objects.create_user(
                username=datos['username'],
                email=datos['email'],
                password=datos['password'],
                first_name=datos['first_name'],
                last_name=datos['last_name']
            )
            
            profile, created = Profile.objects.get_or_create(user=user)
            profile.perfil = datos['perfil']
            profile.telefono = datos['telefono']
            profile.save()
            
            print(f"Usuario {datos['username']} creado como {datos['perfil']}")
            
        except Exception as e:
            print(f"Error creando {datos['username']}: {e}")

if __name__ == '__main__':
    crear_usuarios()
