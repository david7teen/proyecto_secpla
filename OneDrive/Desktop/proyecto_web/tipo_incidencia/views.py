from direccion.models import Direccion
from departamento.models import Departamento
from tipo_incidencia.models import TipoIncidencia
from django.http import JsonResponse

def crear_tipo_incidencia_ajax(request):
    if request.session.get('perfil') != 'SECPLA':
        return JsonResponse({'error': 'Acceso no autorizado'}, status=403)

    if request.method == 'POST':
        nombre = request.POST.get('nombre_tipo')
        direccion_id = request.POST.get('direccion_tipo')
        departamento_id = request.POST.get('departamento_tipo')

        if not all([nombre, direccion_id, departamento_id]):
            return JsonResponse({'error': 'Faltan campos obligatorios'}, status=400)

        try:
            direccion = Direccion.objects.get(id=direccion_id, estado='Activo')
        except Direccion.DoesNotExist:
            return JsonResponse({'error': 'Dirección inválida'}, status=400)

        try:
            departamento = Departamento.objects.get(id=departamento_id, direccion_departamento=direccion, estado='Activo')
        except Departamento.DoesNotExist:
            return JsonResponse({'error': 'Departamento inválido o no pertenece a la dirección'}, status=400)

        tipo = TipoIncidencia.objects.create(
            nombre=nombre,
            descripcion='Sin descripción',
            direccion=direccion,
            departamento=departamento
        )
        return JsonResponse({'id': tipo.id, 'nombre': tipo.nombre})
    return JsonResponse({'error': 'Método no permitido'}, status=405)


