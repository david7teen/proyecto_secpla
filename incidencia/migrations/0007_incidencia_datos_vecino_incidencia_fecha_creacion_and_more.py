import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('incidencia', '0006_incidencia_cuadrilla_asignada'),
        ('tipo_incidencia', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='incidencia',
            name='datos_vecino',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='incidencia',
            name='fecha_creacion',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='incidencia',
            name='fecha_derivacion',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='incidencia',
            name='fecha_finalizacion',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='incidencia',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='incidencias/imagenes/'),
        ),
        migrations.AddField(
            model_name='incidencia',
            name='prioridad',
            field=models.CharField(choices=[('Alta', 'Alta'), ('Normal', 'Normal'), ('Baja', 'Baja')], default='Normal', max_length=10),
        ),
        migrations.AddField(
            model_name='incidencia',
            name='tipo_incidencia',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tipo_incidencia.tipoincidencia'),
        ),
        migrations.AddField(
            model_name='incidencia',
            name='ubicacion',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='incidencia',
            name='descripcion',
            field=models.TextField(default='Sin descripción'),
        ),
    ]
