# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-05 07:36
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('map_basic', '0002_auto_20170605_1534'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('map_map', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LMMap',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('createDate', models.DateTimeField(auto_now_add=True)),
                ('updateDate', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, null=True)),
                ('father_id', models.UUIDField(blank=True, null=True)),
                ('display', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='LMMapPlace',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('createDate', models.DateTimeField(auto_now_add=True)),
                ('updateDate', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, null=True)),
                ('map_father_id', models.UUIDField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='LMUserDetail',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('createDate', models.DateTimeField(auto_now_add=True)),
                ('updateDate', models.DateTimeField(auto_now=True)),
                ('my_follow', models.ManyToManyField(blank=True, related_name='lm_user_detail_follow_lm_map', to='map_map.LMMap')),
                ('my_maps', models.ManyToManyField(blank=True, related_name='lm_user_detail_maps_lm_map', to='map_map.LMMap')),
                ('my_place', models.ManyToManyField(blank=True, related_name='lm_user_detail_lm_map_place', to='map_map.LMMapPlace')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='LMAttraction',
        ),
        migrations.DeleteModel(
            name='LMCity',
        ),
        migrations.DeleteModel(
            name='LMCountry',
        ),
        migrations.DeleteModel(
            name='LMPhoto',
        ),
        migrations.RemoveField(
            model_name='lmplace',
            name='attraction',
        ),
        migrations.RemoveField(
            model_name='lmplace',
            name='city',
        ),
        migrations.RemoveField(
            model_name='lmplace',
            name='country',
        ),
        migrations.RemoveField(
            model_name='lmplace',
            name='photos',
        ),
        migrations.RemoveField(
            model_name='lmplace',
            name='place_type',
        ),
        migrations.RemoveField(
            model_name='lmplace',
            name='rating',
        ),
        migrations.DeleteModel(
            name='LMPlaceType',
        ),
        migrations.DeleteModel(
            name='LMRating',
        ),
        migrations.DeleteModel(
            name='LMPlace',
        ),
        migrations.AddField(
            model_name='lmmapplace',
            name='photos',
            field=models.ManyToManyField(blank=True, related_name='lm_map_place_lm_photo', to='map_basic.LMPhoto'),
        ),
        migrations.AddField(
            model_name='lmmapplace',
            name='place',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='map_basic.LMPlace'),
        ),
        migrations.AddField(
            model_name='lmmap',
            name='attractions',
            field=models.ManyToManyField(blank=True, related_name='lm_map_lm_attraction', to='map_basic.LMAttraction'),
        ),
        migrations.AddField(
            model_name='lmmap',
            name='cities',
            field=models.ManyToManyField(blank=True, related_name='lm_map_lm_city', to='map_basic.LMCity'),
        ),
        migrations.AddField(
            model_name='lmmap',
            name='countries',
            field=models.ManyToManyField(blank=True, related_name='lm_map_lm_country', to='map_basic.LMCountry'),
        ),
        migrations.AddField(
            model_name='lmmap',
            name='photos',
            field=models.ManyToManyField(blank=True, related_name='lm_map_lm_photo', to='map_basic.LMPhoto'),
        ),
        migrations.AddField(
            model_name='lmmap',
            name='place_types',
            field=models.ManyToManyField(blank=True, related_name='lm_map_lm_place_type', to='map_basic.LMPlaceType'),
        ),
        migrations.AddField(
            model_name='lmmap',
            name='places',
            field=models.ManyToManyField(blank=True, related_name='lm_map_lm_map_place', to='map_map.LMMapPlace'),
        ),
        migrations.AddField(
            model_name='lmmap',
            name='rating',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lm_map_lm_rating', to='map_basic.LMRating'),
        ),
        migrations.AddField(
            model_name='lmmap',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]
