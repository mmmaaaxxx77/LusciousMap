import os
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.urls import reverse

from frontend.map_basic.models import LMCountry, LMCity, LMAttraction, LMPlaceType, LMPhoto, LMPlace, LMTag, LMRating


class LMMapPlace(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    createDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=50)
    display = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)
    photos = models.ManyToManyField(LMPhoto, blank=True, related_name='lm_map_place_lm_photo')
    place = models.ForeignKey(LMPlace, null=True, blank=True, on_delete=models.CASCADE)
    map_father_id = models.UUIDField(null=True, blank=True)

    tags = models.ManyToManyField(LMTag, blank=True, related_name='lm_place_lm_tag')
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.DO_NOTHING)

    def as_detail(self):
        return dict(
            model_type="MAPPLACE",
            model_type_ch="地點",
            id=self.id,
            name=self.name,
            display=self.display,
            description=self.description,
            place_type=self.place.place_type.as_json(),
            photos=[h.as_json() for h in list(self.photos.all())],
            rating=self.place.rating.as_json(),
            country=self.place.country.as_json(),
            geo_lat=self.place.geo_lat,
            geo_lng=self.place.geo_lng,
            map_image=self.place.map_image.as_json(),
            tags=[h.as_json() for h in list(self.tags.all())],
            url=reverse('map_place_view', args=[self.id]),
            rating_good_url=reverse('good_place', args=[self.place.id]),
            rating_bad_url=reverse('bad_place', args=[self.place.id]),
            user=dict(username=self.user.username),
            json_url=reverse('detail_mapplace', args=[self.id]),
            g_map_url=self.place.google_map_url,
            webplugin_html='<iframe frameborder="0" width="350" height="300" style="border:none; overflow:hidden; width:350px; height:300px;" allowtransparency="true" src="{}"></iframe>'.
                format(reverse('webplugin_place', args=[self.place.id])),
        )

    def as_search_json(self):
        return dict(
            id=self.id,
            name=self.name,
            display=self.display,
            # tags=self.tags
        )

    def __str__(self):
        return self.name


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
    #cities = models.ManyToManyField(LMCity, blank=True, related_name='lm_map_lm_city')
    #attractions = models.ManyToManyField(LMAttraction, blank=True, related_name='lm_map_lm_attraction')
    place_types = models.ManyToManyField(LMPlaceType, blank=True, related_name='lm_map_lm_place_type')

    photos = models.ManyToManyField(LMPhoto, blank=True, related_name='lm_map_lm_photo')
    places = models.ManyToManyField(LMMapPlace, blank=True, related_name='lm_map_lm_map_place')

    map_image = models.ForeignKey(LMPhoto, null=True, blank=True, on_delete=models.DO_NOTHING,
                                  related_name='lm_map_image_lm_photo')

    tags = models.ManyToManyField(LMTag, blank=True, related_name='lm_map_map_lm_tag')

    def as_detail(self):
        return dict(
            model_type="MAP",
            model_type_ch="地圖",
            id=self.id,
            name=self.name,
            display=self.display,
            country=(self.countries.all()[:1])[0].as_json(),
            type=(self.place_types.all()[:1])[0].as_json(),
            description=self.description,
            photos=[h.as_json() for h in list(self.photos.all())],
            rating=self.rating.as_json(),
            countries=[h.as_json() for h in list(self.countries.all())],
            map_image=None if self.map_image is None else self.map_image.as_json(),
            tags=[h.as_json() for h in list(self.tags.all())],
            user=dict(username=self.user.username),
            url=reverse('map_view', args=[self.id]),
            rating_good_url=reverse('good_map', args=[self.id]),
            rating_bad_url=reverse('bad_map', args=[self.id]),
            json_url=reverse('detail_map', args=[self.id]),
            places=[place.as_detail() for place in self.places.order_by("-createDate").all()],
            webplugin_html='<iframe frameborder="0" width="350" height="300" style="border:none; overflow:hidden; width:350px; height:300px;" allowtransparency="true" src="{}"></iframe>'.
                format(reverse('webplugin_map', args=[self.id])),
        )

    def as_search_json(self):
        return dict(
            id=self.id,
            name=self.name,
            display=self.display,
            # tags=self.tags
        )

    def __str__(self):
        return self.name


@receiver(models.signals.post_delete, sender=LMMap)
def post_delete_lmmap_on_delete(sender, instance, **kwargs):

    if instance.rating:
        instance.rating.delete()


@receiver(models.signals.pre_delete, sender=LMMap)
def pre_delete_lmmap_on_delete(sender, instance, **kwargs):

    for photo in instance.photos.all():
        if os.path.isfile(photo.image.path):
            os.remove(photo.image.path)
        photo.delete()

        if instance.map_image is not None:
            if os.path.isfile(instance.map_image.image.path):
                os.remove(instance.map_image.image.path)
            instance.map_image.delete()


class LMUserDetail(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    createDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    my_place = models.ManyToManyField(LMMapPlace, blank=True, related_name='lm_user_detail_lm_map_place')
    my_maps = models.ManyToManyField(LMMap, blank=True, related_name='lm_user_detail_maps_lm_map')
    my_follow = models.ManyToManyField(LMMap, blank=True, related_name='lm_user_detail_follow_lm_map')

    def as_detail(self):
        return dict(id=self.id,
                    user=dict(id=self.user.id,
                              username=self.user.username,
                              email=self.user.email),
                    my_place=[place.as_detail for place in self.my_place.all()],
                    my_maps=[map.as_detail for map in self.my_map.all()],
                    my_follow=[follow.as_detail for follow in self.my_follow.all()])


    def __str__(self):
        return self.user.username
