# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-26 08:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map_map', '0011_remove_lmmap_places'),
    ]

    operations = [
        migrations.AddField(
            model_name='lmmap',
            name='places',
            field=models.ManyToManyField(blank=True, related_name='lm_map_lm_map_place', to='map_map.LMMapPlace'),
        ),
    ]