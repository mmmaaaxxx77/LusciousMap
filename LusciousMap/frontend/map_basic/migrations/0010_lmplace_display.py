# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-09 17:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map_basic', '0009_auto_20170609_2356'),
    ]

    operations = [
        migrations.AddField(
            model_name='lmplace',
            name='display',
            field=models.BooleanField(default=True),
        ),
    ]