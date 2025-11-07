from django.urls import path
from . import views

urlpatterns = [
    path('crear-tipo-ajax/', views.crear_tipo_incidencia_ajax, name='crear_tipo_incidencia_ajax'),
]