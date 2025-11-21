import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('encuesta', '0010_alter_encuesta_estado'),
        ('tipo_incidencia', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='encuesta',
            name='tipo_incidencia',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='tipo_incidencia.tipoincidencia'),
            preserve_default=False,
        ),
    ]
