from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("encuesta", "0008_alter_encuesta_tipo_incidencia"),
    ]

    operations = [
        migrations.AlterField(
            model_name="encuesta",
            name="datos_vecino",
            field=models.TextField(blank=True, null=True),
        ),
    ]
