import os
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.urls import reverse


class LMTag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=25)
    createDate = models.DateTimeField(auto_now_add=True)

    createUser = models.ForeignKey(User, null=True, blank=True, on_delete=models.DO_NOTHING)

    def __str__(self):
       return self.name

    def as_json(self):
        return dict(id=self.id, name=self.name)


class LMCountry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    long_name = models.CharField(max_length=50)
    short_name = models.CharField(max_length=25, blank=True, null=True)
    long_name_en = models.CharField(max_length=50, blank=True, null=True)
    short_name_en = models.CharField(max_length=25, blank=True, null=True)
    geo_lat = models.FloatField(default=0)
    geo_lng = models.FloatField(default=0)
    createDate = models.DateTimeField(auto_now_add=True)

    def as_json(self):
        return dict(
            id=self.id,
            long_name=self.long_name,
            short_name=self.short_name,
            geo_lat=self.geo_lat,
            geo_lng=self.geo_lng
        )

    def __str__(self):
       return self.long_name


class LMCity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    long_name = models.CharField(max_length=50)
    short_name = models.CharField(max_length=25, blank=True, null=True)
    long_name_en = models.CharField(max_length=50, blank=True, null=True)
    short_name_en = models.CharField(max_length=25, blank=True, null=True)
    geo_lat = models.FloatField(default=0)
    geo_lng = models.FloatField(default=0)
    createDate = models.DateTimeField(auto_now_add=True)

    def as_json(self):
        return dict(
            id=self.id,
            long_name=self.long_name,
            short_name=self.short_name,
            geo_lat=self.geo_lat,
            geo_lng=self.geo_lng
        )

    def __str__(self):
       return self.long_name


class LMAttraction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    long_name = models.CharField(max_length=50)
    short_name = models.CharField(max_length=25, blank=True, null=True)
    long_name_en = models.CharField(max_length=50, blank=True, null=True)
    short_name_en = models.CharField(max_length=25, blank=True, null=True)
    geo_lat = models.FloatField(default=0)
    geo_lng = models.FloatField(default=0)
    createDate = models.DateTimeField(auto_now_add=True)

    def as_json(self):
        return dict(
            id=self.id,
            long_name=self.long_name,
            short_name=self.short_name,
            geo_lat=self.geo_lat,
            geo_lng=self.geo_lng
        )

    def __str__(self):
       return self.long_name


class LMPhoto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='photos')
    createDate = models.DateTimeField(auto_now_add=True)

    def image_url(self):
        return reverse('get_photo', args=[self.id])

    def __str__(self):
       return self.image.name

    def as_json(self):
        return dict(
            id=self.id,
            image=dict(
                name=str(self.image.name),
                path=str(self.image.path),
            ),
            image_url=reverse('get_photo', args=[self.id]),
            image_thumbnail_url=reverse('get_photothumbnail', args=[self.id])
        )


@receiver(models.signals.post_delete, sender=LMPhoto)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    try:
        if instance.image:
            if os.path.isfile(instance.image.path):
                os.remove(instance.image.path)
    except:
        print("instance.image")


class LMRating(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    createDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(auto_now=True)

    good = models.ManyToManyField(User, blank=True, related_name='rating_good_user')
    bad = models.ManyToManyField(User, blank=True, related_name='rating_bad_user')

    def as_json(self):
        return dict(id=self.id, good=self.good.count(), bad=self.bad.count())


class LMPlaceType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    createDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=10)
    name_en = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
       return self.name

    def as_json(self):
        return dict(id=self.id, name=self.name, name_en=self.name_en)

"""
class LMPlaceManager(models.Manager):
    def delete(self):
        self.
        self.delete()
"""


class LMPlace(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    createDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=50)
    display = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)
    place_type = models.ForeignKey(LMPlaceType, null=True, blank=True, on_delete=models.DO_NOTHING,
                                   related_name='lm_place_lm_place_type')
    photos = models.ManyToManyField(LMPhoto, blank=True, related_name='lm_photo_ids')
    rating = models.OneToOneField(LMRating, null=True, blank=True, on_delete=models.CASCADE)

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

    map_image = models.ForeignKey(LMPhoto, null=True, blank=True, on_delete=models.CASCADE,
                                  related_name='lm_place_image_lm_photo')

    tags = models.ManyToManyField(LMTag, blank=True, related_name='lm_map_place_lm_tag')
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.DO_NOTHING)

    def __str__(self):
       return "{}, {}".format(self.name, self.country)

    def as_detail(self):
        return dict(
            model_type="PLACE",
            model_type_ch="地點",
            id=self.id,
            name=self.name,
            display=self.display,
            description=self.description,
            place_type=self.place_type.as_json(),
            photos=[h.as_json() for h in list(self.photos.all())],
            rating=self.rating.as_json(),
            country=self.country.as_json(),
            geo_lat=self.geo_lat,
            geo_lng=self.geo_lng,
            map_image=None if self.map_image is None else self.map_image.as_json(),
            tags=[h.as_json() for h in list(self.tags.all())],
            url=reverse('place_view', args=[self.id]),
            rating_good_url=reverse('good_place', args=[self.id]),
            rating_bad_url=reverse('bad_place', args=[self.id]),
            user=dict(username=""),
            g_map_url=self.google_map_url,
            webplugin_html='<iframe frameborder="0" width="350" height="300" style="border:none; overflow:hidden; width:350px; height:300px;" allowtransparency="true" src="{}"></iframe>'.
                format(reverse('webplugin_place', args=[self.id])),
        )

    def as_search_json_view(self):
        return dict(
            id=self.id,
            long_name=self.name,
            short_name=self.name,
            geo_lat=self.geo_lat,
            geo_lng=self.geo_lng,
            address=self.google_address,
            place_id=self.google_place_id,
        )

    def as_search_json(self):
        return dict(
            id=self.id,
            name=self.name,
            display=self.display,
        )


@receiver(models.signals.post_delete, sender=LMPlace)
def post_delete_lmplace_on_delete(sender, instance, **kwargs):

    try:
        if instance.rating:
            instance.rating.delete()
    except:
        print("no instance.rating")

    """
    for mpaplace in LMMapPlace.objects.filter(place__exact=instance):
        mpaplace.delete()
    """


@receiver(models.signals.pre_delete, sender=LMPlace)
def pre_delete_lmplace_on_delete(sender, instance, **kwargs):

    try:
        for photo in instance.photos.all():
            if os.path.isfile(photo.image.path):
                os.remove(photo.image.path)
            photo.delete()
    except:
        print("delete photo exception")
    try:
        if instance.map_image is not None:
            if os.path.isfile(instance.map_image.image.path):
                os.remove(instance.map_image.image.path)
            instance.map_image.delete()
    except:
        print("delete map photo exception")


    #instance.photos.all().delete()
