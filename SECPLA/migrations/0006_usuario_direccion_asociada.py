import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("SECPLA", "0005_usuario_departamento_asociado"),
        ("direccion", "0002_rename_nombre_direccion_nombre_direccion_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="usuario",
            name="direccion_asociada",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="direccion.direccion",
            ),
        ),
    ]
