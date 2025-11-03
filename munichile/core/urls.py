from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('check_profile', views.check_profile, name='check_profile'),
    
    
    path('dashboard/secpla/', views.dashboard_secpla, name='dashboard_secpla'),
    path('dashboard/territorial/', views.dashboard_territorial, name='dashboard_territorial'),
    path('dashboard/direccion/', views.dashboard_direccion, name='dashboard_direccion'),
    path('dashboard/departamento/', views.dashboard_departamento, name='dashboard_departamento'),
    path('dashboard/cuadrilla/', views.dashboard_cuadrilla, name='dashboard_cuadrilla'),
]
