from django.shortcuts import render, redirect
from SECPLA.models import Usuario
from incidencia.models import Incidencia

def vista_departamento(request):
    usuario_activo_data = request.session.get('usuario_activo')
    if not usuario_activo_data:
        return redirect('/secpla/login/departamento/')
    
    departamento = Usuario.objects.get(id=usuario_activo_data['id'])

    # Aquí necesitas lógica para obtener las incidencias del departamento
    # Esto depende de cómo esté estructurado tu modelo
    incidencias = Incidencia.objects.all()  # Temporal

    resumen = {
        'pendientes': incidencias.filter(estado='Pendiente').count(),
        'derivadas': incidencias.filter(estado='Derivada').count(),
        'rechazadas': incidencias.filter(estado='Rechazada').count(),
        'finalizadas': incidencias.filter(estado='Finalizada').count(),
    }

    return render(request, 'Departamento/dashboard_departamento.html', {
        'usuario_activo': departamento,
        'resumen': resumen
    })

def incidencias_pendientes_departamento(request):
    usuario_activo = request.session.get('usuario_activo')
    departamento = Usuario.objects.get(id=usuario_activo['id'])
    pendientes = Incidencia.objects.filter(departamento_incidencia=departamento, estado='Pendiente')
    cuadrillas = Usuario.objects.filter(perfil='Cuadrilla')

    return render(request, 'Departamento/listado_incidencias_departamento.html', {
        'estado': estado,
        'incidencias': incidencias,
        'cuadrillas': cuadrillas,
        'usuario_activo': departamento
    })

def derivar_incidencia(request, incidencia_id):
    if request.method == 'POST':
        cuadrilla_id = request.POST.get('cuadrilla_id')
        incidencia = Incidencia.objects.get(id=incidencia_id)
        cuadrilla = Usuario.objects.get(id=cuadrilla_id)

        incidencia.cuadrilla_asignada = cuadrilla
        incidencia.estado = 'Derivada'
        incidencia.save()

    return redirect('/departamento/incidencias/pendientes/')
