import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("encuesta", "0007_alter_encuesta_tipo_incidencia"),
        ("tipo_incidencia", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="encuesta",
            name="tipo_incidencia",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="tipo_incidencia.tipoincidencia",
            ),
        ),
    ]
