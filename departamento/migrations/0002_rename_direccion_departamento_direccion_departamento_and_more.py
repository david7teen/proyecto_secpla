from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("departamento", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="departamento",
            old_name="direccion",
            new_name="direccion_departamento",
        ),
        migrations.RenameField(
            model_name="departamento",
            old_name="encargado",
            new_name="encargado_departamento",
        ),
        migrations.RenameField(
            model_name="departamento",
            old_name="nombre",
            new_name="nombre_departamento",
        ),
    ]
