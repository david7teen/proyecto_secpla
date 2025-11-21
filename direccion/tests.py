from django.test import TestCase, Client
from django.urls import reverse
from SECPLA.models import Usuario
from direccion.models import Direccion
from incidencia.models import Incidencia

class DireccionViewsTestCase(TestCase):

    def setUp(self):
        # Crear usuario y dirección de prueba
        self.client = Client()
        self.direccion = Direccion.objects.create(nombre_direccion="Dirección de Prueba")
        self.usuario = Usuario.objects.create(
            username="direccion_user",
            perfil="Dirección",
            direccion_asociada=self.direccion
        )
        self.client.session['usuario_activo'] = {
            'id': self.usuario.id,
            'perfil': self.usuario.perfil
        }
        self.client.session.save()

        # Crear incidencias de prueba
        Incidencia.objects.create(nombre_incidencia="Incidencia 1", estado="Abierta", direccion_incidencia=self.direccion)
        Incidencia.objects.create(nombre_incidencia="Incidencia 2", estado="Derivada", direccion_incidencia=self.direccion)
        Incidencia.objects.create(nombre_incidencia="Incidencia 3", estado="Finalizada", direccion_incidencia=self.direccion)

    def test_incidencias_pendientes_view(self):
        response = self.client.get(reverse('dir_incidencias_pendientes'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Incidencia 1")

    def test_incidencias_derivadas_view(self):
        response = self.client.get(reverse('dir_incidencias_derivadas'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Incidencia 2")

    def test_incidencias_finalizadas_view(self):
        response = self.client.get(reverse('dir_incidencias_finalizadas'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Incidencia 3")