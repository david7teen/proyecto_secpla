from django.contrib import admin
from django.urls import path, include
from home.urls import home_urlpatterns
from django.conf import settings
from django.conf.urls.static import static

# Importar vistas principales de perfiles
from SECPLA.views import (
    vista_secpla, vista_direccion, vista_departamento,
    vista_territorial, vista_cuadrilla
)

urlpatterns = [
    # Página principal (home)
    path('', include(home_urlpatterns)),

    # Panel de administración
    path('admin/', admin.site.urls),

    # Módulos principales
    path('secpla/', include('SECPLA.urls')),
    path('territorial/', include('territorial.urls')),
    path('direccion/', include('direccion.urls')),
    path('departamento/', include('departamento.urls')),
    path('cuadrilla/', include('cuadrilla.urls')),
    path('tipo_incidencia/', include('tipo_incidencia.urls')),

    # Perfiles
    path('perfil/secpla/', vista_secpla, name='dashboard_secpla'),
    path('perfil/direccion/', vista_direccion, name='dashboard_direccion'),
    path('perfil/departamento/', vista_departamento, name='dashboard_departamento'),
    path('perfil/territorial/', vista_territorial, name='dashboard_territorial'),
    path('perfil/cuadrilla/', vista_cuadrilla, name='dashboard_cuadrilla'),
]

# Archivos multimedia
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
