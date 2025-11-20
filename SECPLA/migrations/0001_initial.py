from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Usuario",
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
                ("apellido", models.CharField(max_length=100)),
                ("correo", models.EmailField(max_length=254)),
                ("telefono", models.CharField(max_length=20)),
                (
                    "perfil",
                    models.CharField(
                        choices=[
                            ("SECPLA", "SECPLA"),
                            ("Dirección", "Dirección"),
                            ("Departamento", "Departamento"),
                            ("Territorial", "Territorial"),
                            ("Cuadrilla", "Cuadrilla"),
                        ],
                        max_length=50,
                    ),
                ),
                ("contraseña", models.CharField(max_length=100)),
                ("estado", models.CharField(default="Activo", max_length=20)),
            ],
        ),
    ]
