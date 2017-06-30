# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-07 09:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map_basic', '0002_auto_20170605_1534'),
    ]

    operations = [
        migrations.AddField(
            model_name='lmattraction',
            name='geo_lat',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='lmattraction',
            name='geo_lng',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='lmcity',
            name='geo_lat',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='lmcity',
            name='geo_lng',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='lmcountry',
            name='geo_lat',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='lmcountry',
            name='geo_lng',
            field=models.FloatField(default=0),
        ),
    ]
