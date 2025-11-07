from django.contrib import admin
from django.urls import path, include
from home.urls import home_urlpatterns
from SECPLA.views import vista_secpla, vista_direccion, vista_cuadrilla, vista_departamento, vista_territorial
from django.conf import settings
from django.conf.urls.static import static
from territorial.views import vista_territorial


urlpatterns = [
    path('',include(home_urlpatterns)),
    path("admin/", admin.site.urls),
    path('secpla/', include('SECPLA.urls')),
    path('territorial/', include('territorial.urls')),
    path('perfil/secpla/', vista_secpla, name='dashboard_secpla'),
    path('perfil/direccion/', vista_direccion, name='dashboard_direccion'),
    path('perfil/departamento/', vista_departamento, name='dashboard_departamento'),
    path('perfil/territorial/', vista_territorial, name='dashboard_territorial'),
    path('perfil/cuadrilla/', vista_cuadrilla, name='dashboard_cuadrilla'),
    path('tipo_incidencia/', include('tipo_incidencia.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
