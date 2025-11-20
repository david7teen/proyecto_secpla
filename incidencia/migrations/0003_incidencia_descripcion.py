from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "incidencia",
            "0002_rename_departamento_incidencia_departamento_incidencia_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="incidencia",
            name="descripcion",
            field=models.CharField(default="Sin descripción", max_length=200),
        ),
    ]
