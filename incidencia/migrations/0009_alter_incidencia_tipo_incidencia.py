import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('incidencia', '0008_incidencia_audio_incidencia_video'),
        ('tipo_incidencia', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incidencia',
            name='tipo_incidencia',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='tipo_incidencia.tipoincidencia'),
            preserve_default=False,
        ),
    ]
