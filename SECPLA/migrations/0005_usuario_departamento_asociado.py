import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("SECPLA", "0004_remove_usuario_direccion_asociada"),
        ("departamento", "0003_departamento_estado"),
    ]

    operations = [
        migrations.AddField(
            model_name="usuario",
            name="departamento_asociado",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="usuarios_asociados",
                to="departamento.departamento",
            ),
        ),
    ]
