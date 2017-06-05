# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-05 06:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LMAttraction',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('long_name', models.CharField(max_length=50)),
                ('short_name', models.CharField(blank=True, max_length=25, null=True)),
                ('long_name_en', models.CharField(blank=True, max_length=50, null=True)),
                ('short_name_en', models.CharField(blank=True, max_length=25, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='LMCity',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('long_name', models.CharField(max_length=50)),
                ('short_name', models.CharField(blank=True, max_length=25, null=True)),
                ('long_name_en', models.CharField(blank=True, max_length=50, null=True)),
                ('short_name_en', models.CharField(blank=True, max_length=25, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='LMCountry',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('long_name', models.CharField(max_length=50)),
                ('short_name', models.CharField(blank=True, max_length=25, null=True)),
                ('long_name_en', models.CharField(blank=True, max_length=50, null=True)),
                ('short_name_en', models.CharField(blank=True, max_length=25, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='LMPhoto',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to='photos')),
                ('createDate', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='LMPlace',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('createDate', models.DateTimeField(auto_now_add=True)),
                ('updateDate', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, null=True)),
                ('geo_lat', models.FloatField(default=0)),
                ('geo_lng', models.FloatField(default=0)),
                ('opening_hours_weekday_text', models.TextField(blank=True, null=True)),
                ('google_place_id', models.CharField(blank=True, max_length=100, null=True)),
                ('google_id', models.CharField(blank=True, max_length=100, null=True)),
                ('google_rating', models.FloatField(default=0)),
                ('google_map_url', models.CharField(blank=True, max_length=255, null=True)),
                ('google_website', models.CharField(blank=True, max_length=255, null=True)),
                ('google_phone_number', models.CharField(blank=True, max_length=50, null=True)),
                ('google_international_phone_number', models.CharField(blank=True, max_length=50, null=True)),
                ('google_address', models.CharField(blank=True, max_length=255, null=True)),
                ('attraction', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='map_basic.LMAttraction')),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='map_basic.LMCity')),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='map_basic.LMCountry')),
                ('photos', models.ManyToManyField(blank=True, related_name='photo_ids', to='map_basic.LMPhoto')),
            ],
        ),
        migrations.CreateModel(
            name='LMPlaceType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('createDate', models.DateTimeField(auto_now_add=True)),
                ('updateDate', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=10)),
                ('name_en', models.CharField(blank=True, max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='LMRating',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('createDate', models.DateTimeField(auto_now_add=True)),
                ('updateDate', models.DateTimeField(auto_now=True)),
                ('total', models.IntegerField(default=0)),
                ('good', models.IntegerField(default=0)),
                ('bad', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='lmplace',
            name='place_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='place_place_type', to='map_basic.LMPlaceType'),
        ),
        migrations.AddField(
            model_name='lmplace',
            name='rating',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='place_rating', to='map_basic.LMPlaceType'),
        ),
    ]
