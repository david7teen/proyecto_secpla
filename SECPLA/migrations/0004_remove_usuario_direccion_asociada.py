from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("SECPLA", "0003_usuario_direccion_asociada"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="usuario",
            name="direccion_asociada",
        ),
    ]
