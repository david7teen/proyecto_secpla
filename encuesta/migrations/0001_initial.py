from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Encuesta",
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
                ("nombre_encuesta", models.CharField(max_length=100)),
                ("descripcion_incidente", models.TextField()),
                ("ubicacion", models.CharField(max_length=200)),
                ("imagen", models.URLField(blank=True, null=True)),
                ("video", models.URLField(blank=True, null=True)),
                ("audio", models.URLField(blank=True, null=True)),
                ("pregunta", models.TextField()),
                ("prioridad", models.CharField(max_length=50)),
                ("datos_vecino", models.TextField()),
                ("tipo_incidencia", models.CharField(max_length=100)),
                ("estado", models.CharField(default="Activo", max_length=20)),
            ],
        ),
    ]
