import uuid

from django.contrib.auth.models import User
from django.db import models

from frontend.map_basic.models import LMRating, LMCountry, LMCity, LMAttraction, LMPlaceType, LMPhoto, LMPlace


class LMMapPlace(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    createDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    photos = models.ManyToManyField(LMPhoto, blank=True, related_name='lm_map_place_lm_photo')
    place = models.ForeignKey(LMPlace, null=True, blank=True, on_delete=models.DO_NOTHING)
    map_father_id = models.UUIDField(null=True, blank=True)


class LMMap(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    createDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.DO_NOTHING)
    # auth = models.ManyToManyField(User, blank=True, related_name='lmmap_user')
    father_id = models.UUIDField(null=True, blank=True)
    display = models.BooleanField(default=True)
    rating = models.ForeignKey(LMRating, null=True, blank=True, on_delete=models.CASCADE,
                               related_name='lm_map_lm_rating')
    countries = models.ManyToManyField(LMCountry, blank=True, related_name='lm_map_lm_country')
    cities = models.ManyToManyField(LMCity, blank=True, related_name='lm_map_lm_city')
    attractions = models.ManyToManyField(LMAttraction, blank=True, related_name='lm_map_lm_attraction')
    place_types = models.ManyToManyField(LMPlaceType, blank=True, related_name='lm_map_lm_place_type')

    photos = models.ManyToManyField(LMPhoto, blank=True, related_name='lm_map_lm_photo')
    places = models.ManyToManyField(LMMapPlace, blank=True, related_name='lm_map_lm_map_place')


class LMUserDetail(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    createDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    my_place = models.ManyToManyField(LMMapPlace, blank=True, related_name='lm_user_detail_lm_map_place')
    my_maps = models.ManyToManyField(LMMap, blank=True, related_name='lm_user_detail_maps_lm_map')
    my_follow = models.ManyToManyField(LMMap, blank=True, related_name='lm_user_detail_follow_lm_map')
