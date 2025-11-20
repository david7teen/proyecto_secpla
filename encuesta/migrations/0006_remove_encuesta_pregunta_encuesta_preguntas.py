from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("encuesta", "0005_encuesta_categoria"),
        ("pregunta", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="encuesta",
            name="pregunta",
        ),
        migrations.AddField(
            model_name="encuesta",
            name="preguntas",
            field=models.ManyToManyField(to="pregunta.pregunta"),
        ),
    ]
