import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("departamento", "__first__"),
        ("direccion", "__first__"),
    ]

    operations = [
        migrations.CreateModel(
            name="Incidencia",
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
                ("nombre", models.CharField(max_length=100)),
                (
                    "estado",
                    models.CharField(
                        choices=[
                            ("Creada", "Creada"),
                            ("Derivada", "Derivada"),
                            ("Rechazada", "Rechazada"),
                            ("Finalizada", "Finalizada"),
                        ],
                        default="Creada",
                        max_length=20,
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
        ),
    ]
