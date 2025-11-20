from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Direccion",
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
                ("encargado", models.CharField(max_length=100)),
                ("correo_encargado", models.EmailField(max_length=254)),
                (
                    "estado",
                    models.CharField(
                        choices=[("Activo", "Activo"), ("Inactivo", "Inactivo")],
                        default="Activo",
                        max_length=20,
                    ),
                ),
            ],
        ),
    ]
