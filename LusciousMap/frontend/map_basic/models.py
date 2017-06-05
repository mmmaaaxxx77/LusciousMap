import uuid

from django.db import models


class LMCountry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    long_name = models.CharField(max_length=50)
    short_name = models.CharField(max_length=25, blank=True, null=True)
    long_name_en = models.CharField(max_length=50, blank=True, null=True)
    short_name_en = models.CharField(max_length=25, blank=True, null=True)


class LMCity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    long_name = models.CharField(max_length=50)
    short_name = models.CharField(max_length=25, blank=True, null=True)
    long_name_en = models.CharField(max_length=50, blank=True, null=True)
    short_name_en = models.CharField(max_length=25, blank=True, null=True)


class LMAttraction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    long_name = models.CharField(max_length=50)
    short_name = models.CharField(max_length=25, blank=True, null=True)
    long_name_en = models.CharField(max_length=50, blank=True, null=True)
    short_name_en = models.CharField(max_length=25, blank=True, null=True)


class LMPhoto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='photos')
    createDate = models.DateTimeField(auto_now_add=True)


class LMRating(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    createDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(auto_now=True)

    total = models.IntegerField(default=0)
    good = models.IntegerField(default=0)
    bad = models.IntegerField(default=0)


class LMPlaceType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    createDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=10)
    name_en = models.CharField(max_length=10, blank=True, null=True)


class LMPlace(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    createDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    place_type = models.ForeignKey(LMPlaceType, null=True, blank=True, on_delete=models.DO_NOTHING,
                                   related_name='lm_place_lm_place_type')
    photos = models.ManyToManyField(LMPhoto, blank=True, related_name='lm_photo_ids')
    rating = models.ForeignKey(LMRating, null=True, blank=True, on_delete=models.CASCADE,
                               related_name='lm_place_lm_rating')

    country = models.ForeignKey(LMCountry, null=True, blank=True, on_delete=models.DO_NOTHING)
    city = models.ForeignKey(LMCity, null=True, blank=True, on_delete=models.DO_NOTHING)
    attraction = models.ForeignKey(LMAttraction, null=True, blank=True, on_delete=models.DO_NOTHING)

    geo_lat = models.FloatField(default=0)
    geo_lng = models.FloatField(default=0)

    opening_hours_weekday_text = models.TextField(blank=True, null=True)
    google_place_id = models.CharField(max_length=100, blank=True, null=True)
    google_id = models.CharField(max_length=100, blank=True, null=True)
    google_rating = models.FloatField(default=0)
    google_map_url = models.CharField(max_length=255, blank=True, null=True)
    google_website = models.CharField(max_length=255, blank=True, null=True)
    google_phone_number = models.CharField(max_length=50, blank=True, null=True)
    google_international_phone_number = models.CharField(max_length=50, blank=True, null=True)
    google_address = models.CharField(max_length=255, blank=True, null=True)



