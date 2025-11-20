import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("encuesta", "0006_remove_encuesta_pregunta_encuesta_preguntas"),
        ("tipo_incidencia", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="encuesta",
            name="tipo_incidencia",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="tipo_incidencia.tipoincidencia",
            ),
        ),
    ]
