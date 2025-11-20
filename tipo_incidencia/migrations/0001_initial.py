import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("SECPLA", "0003_usuario_direccion_asociada"),
        ("departamento", "0003_departamento_estado"),
        ("direccion", "0002_rename_nombre_direccion_nombre_direccion_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="TipoIncidencia",
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
                ("nombre", models.CharField(max_length=100, unique=True)),
                (
                    "descripcion",
                    models.CharField(default="Sin descripción", max_length=200),
                ),
                ("fecha_creacion", models.DateTimeField(auto_now_add=True)),
                (
                    "creado_por",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="tipos_incidencia_creados",
                        to="SECPLA.usuario",
                    ),
                ),
                (
                    "departamento",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="departamento.departamento",
                    ),
                ),
                (
                    "direccion",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="direccion.direccion",
                    ),
                ),
            ],
            options={
                "verbose_name": "Tipo de Incidencia",
                "verbose_name_plural": "Tipos de Incidencia",
                "ordering": ["nombre"],
            },
        ),
    ]
