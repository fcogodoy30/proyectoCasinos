# Generated by Django 5.0.6 on 2024-06-03 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicio', '0002_delete_usuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='casinocolacion',
            name='visible',
            field=models.IntegerField(choices=[(0, 'No'), (1, 'Sí')], default=1),
        ),
    ]