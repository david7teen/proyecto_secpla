
from django.urls import path
from gestion import views

gestion_urlpatterns = [
    path('main_usuario/', views.main_usuario, name='main_usuario'),
    path('encuesta/crear/', views.crear_encuesta, name='crear_encuesta'),
]