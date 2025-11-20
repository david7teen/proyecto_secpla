from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("SECPLA", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="RecuperacionIntento",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("correo", models.EmailField(max_length=254)),
                ("perfil", models.CharField(max_length=50)),
                ("fecha", models.DateTimeField(auto_now_add=True)),
                ("estado", models.CharField(default="Pendiente", max_length=20)),
                ("observacion", models.TextField(blank=True)),
            ],
        ),
    ]
