# Generated by Django 5.1.6 on 2025-02-11 23:44

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formulario', '0005_alter_avaliacao_categoria'),
    ]

    operations = [
        migrations.AddField(
            model_name='avaliacao',
            name='data_criacao',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='usuario',
            name='data_criacao',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
