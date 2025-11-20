from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("encuesta", "0009_alter_encuesta_datos_vecino"),
    ]

    operations = [
        migrations.AlterField(
            model_name="encuesta",
            name="estado",
            field=models.CharField(
                choices=[
                    ("Abierta", "Abierta"),
                    ("Derivada", "Derivada"),
                    ("En Proceso", "En Proceso"),
                    ("Finalizada", "Finalizada"),
                    ("Cerrada", "Cerrada"),
                    ("Rechazada", "Rechazada"),
                ],
                default="Abierta",
                max_length=20,
            ),
        ),
    ]
