# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-27 15:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_auto_20170926_1402'),
    ]

    operations = [
        migrations.AddField(
            model_name='alerta',
            name='idUbicacion',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='dashboard.Ubicacion'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='alerta',
            name='time',
            field=models.TimeField(default="06:00", verbose_name='time'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='alerta',
            name='tipoAlerta',
            field=models.CharField(default='error temeratura', max_length=128, verbose_name='tipoAlerta'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tipo',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='ubicacion',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]