from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("incidencia", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="incidencia",
            old_name="departamento",
            new_name="departamento_incidencia",
        ),
        migrations.RenameField(
            model_name="incidencia",
            old_name="direccion",
            new_name="direccion_incidencia",
        ),
        migrations.RenameField(
            model_name="incidencia",
            old_name="nombre",
            new_name="nombre_incidencia",
        ),
    ]
