from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Territorial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_territorial', models.CharField(max_length=100)),
                ('apellido_territorial', models.CharField(max_length=100)),
                ('correo_territorial', models.EmailField(max_length=254)),
                ('telefono_territorial', models.CharField(max_length=100)),
                ('estado', models.CharField(default='Activo', max_length=20)),
            ],
        ),
    ]
