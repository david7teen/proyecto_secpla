import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'muni.settings')
django.setup()

from django.contrib.auth.models import User

def borrar_usuarios():
    count_before = User.objects.count()
    print(f"Usuarios antes: {count_before}")
    
    usuarios = User.objects.all()
    for usuario in usuarios:
        print(f"Borrando: {usuario.username} ({usuario.email})")
    
    confirmar = input("¿Estás seguro de borrar TODOS los usuarios? (si/no): ")
    if confirmar.lower() == 'si':
        User.objects.all().delete()
        print("Todos los usuarios borrados")
    else:
        print("Operación cancelada")
    
    print(f"Usuarios después: {User.objects.count()}")

if __name__ == '__main__':
    borrar_usuarios()
