from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "departamento",
            "0002_rename_direccion_departamento_direccion_departamento_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="departamento",
            name="estado",
            field=models.CharField(default="Activo", max_length=20),
        ),
    ]
