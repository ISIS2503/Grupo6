# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-27 14:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_auto_20170926_1402'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensor',
            name='estado',
            field=models.CharField(max_length=1, null=True, verbose_name='estado'),
        ),
    ]
