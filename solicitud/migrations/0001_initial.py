import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("SECPLA", "0003_usuario_direccion_asociada"),
        ("encuesta", "0008_alter_encuesta_tipo_incidencia"),
    ]

    operations = [
        migrations.CreateModel(
            name="Solicitud",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("fecha_creacion", models.DateTimeField(auto_now_add=True)),
                (
                    "estado",
                    models.CharField(
                        choices=[
                            ("Derivada", "Derivada"),
                            ("En proceso", "En proceso"),
                            ("Finalizada", "Finalizada"),
                            ("Rechazada", "Rechazada"),
                            ("Cerrada", "Cerrada"),
                        ],
                        default="Derivada",
                        max_length=20,
                    ),
                ),
                (
                    "evidencia_imagen",
                    models.ImageField(
                        blank=True, null=True, upload_to="solicitudes/evidencia/"
                    ),
                ),
                ("descripcion_resolucion", models.TextField(blank=True, null=True)),
                (
                    "creada_por",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="SECPLA.usuario"
                    ),
                ),
                (
                    "encuesta",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="encuesta.encuesta",
                    ),
                ),
            ],
        ),
    ]
