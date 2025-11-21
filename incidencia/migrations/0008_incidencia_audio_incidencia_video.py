from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('incidencia', '0007_incidencia_datos_vecino_incidencia_fecha_creacion_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='incidencia',
            name='audio',
            field=models.FileField(blank=True, null=True, upload_to='incidencias/audios/'),
        ),
        migrations.AddField(
            model_name='incidencia',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='incidencias/videos/'),
        ),
    ]
