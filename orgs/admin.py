from django.contrib import admin
from .models import Direccion, Departamento, Cuadrilla

# Register your models here.
admin.site.register(Direccion)
admin.site.register(Departamento)
admin.site.register(Cuadrilla)