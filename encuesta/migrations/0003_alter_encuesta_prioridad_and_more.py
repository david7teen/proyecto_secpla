import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("encuesta", "0002_alter_encuesta_audio_alter_encuesta_imagen_and_more"),
        ("incidencia", "0004_alter_incidencia_estado"),
    ]

    operations = [
        migrations.AlterField(
            model_name="encuesta",
            name="prioridad",
            field=models.CharField(
                choices=[("Alta", "Alta"), ("Normal", "Normal"), ("Baja", "Baja")],
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="encuesta",
            name="tipo_incidencia",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="incidencia.incidencia"
            ),
        ),
    ]
