from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("incidencia", "0003_incidencia_descripcion"),
    ]

    operations = [
        migrations.AlterField(
            model_name="incidencia",
            name="estado",
            field=models.CharField(
                choices=[
                    ("Creada", "Creada"),
                    ("Derivada", "Derivada"),
                    ("Rechazada", "Rechazada"),
                    ("Finalizada", "Finalizada"),
                ],
                default="Activo",
                max_length=20,
            ),
        ),
    ]
