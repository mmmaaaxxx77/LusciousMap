import random

from PIL import Image, ImageOps
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.dispatch import receiver
from allauth.account.signals import user_signed_up

from frontend.google_service.models import ServiceKey
from frontend.google_service.views import service_key_getter
from frontend.map_basic.models import LMPlaceType, LMCountry, LMCity, LMAttraction, LMPhoto, LMPlace
from frontend.map_map.models import LMUserDetail, LMMap, LMMapPlace


def index(request):
    if request.user.is_authenticated:
        details = LMUserDetail.objects.filter(user_id__exact=request.user.id).all()
        if len(list(details)) == 0:
            detail = LMUserDetail()
            detail.user = request.user
            detail.save()
    """
    try:
        social_user = SocialAccount.objects.get(user__exact=request.user)
        print(social_user.uid)
        #user = request.user
        #user.username = user.first_name + user.last_name
        #user.save()
    except:
        pass
    print(request.user.username)
    """

    return render(request, "index/index.html", {})


def new_place(request):
    # type
    types = LMPlaceType.objects.order_by("createDate").all()
    # 國家
    countries = LMCountry.objects.order_by("createDate").all()

    form_options = {
        "types": types,
        "countries": countries,
    }

    return render(request, "place/new_place.html", dict(map_key=service_key_getter(0),
                                                        form_options=form_options))


def place_view(request, place_id):
    try:
        place = LMPlace.objects.get(id__exact=place_id)
    except:
        place_o = LMMapPlace.objects.get(id__exact=place_id)
        place = place_o.place
        place.name = place_o.name
        place.description = place_o.description
        if place.photos.count() == 0:
            photos = [].extend([p.as_json() for p in place.place.photos.all()])
        else:
            photos = [h.as_json() for h in list(place.photos.all())]
        place.photos = photos
        #place.tags = place_o.tags

    return render(request, "place/place_view.html", dict(map_key=service_key_getter(0), place=place))


def map_view(request, map_id):
    map = LMMap.objects.get(id__exact=map_id)
    return render(request, "place/map_view.html", dict(map_key=service_key_getter(0),
                                                       map=dict(map=map.as_detail(),
                                                                id=map_id,
                                                                url=reverse('detail_map', args=[map_id]))))


@login_required
def map_edit(request):
    return render(request, "place/map_edit.html", dict(map_key=service_key_getter(0)))


def get_photo(request, image_id):
    photo = LMPhoto.objects.get(id__exact=image_id)

    if 'width' in request.GET.keys() and 'height' in request.GET.keys():
        image = Image.open(photo.image.path)
        size = (int(request.GET['width']), int(request.GET['height']))
        thumb = ImageOps.fit(image, size, Image.ANTIALIAS)

        response = HttpResponse(content_type="image/png")
        thumb.save(response, "PNG")

        return response
    else:
        with open(photo.image.path, "rb") as f:
            return HttpResponse(f.read(), content_type="image/png")


def get_photo_thumbnail(request, image_id):
    photo = LMPhoto.objects.get(id__exact=image_id)

    if 'width' in request.GET.keys() and 'height' in request.GET.keys():
        image = Image.open(photo.image.path)
        size = (int(request.GET['width']), int(request.GET['height']))
        thumb = ImageOps.fit(image, size, Image.ANTIALIAS)

        response = HttpResponse(content_type="image/png")
        thumb.save(response, "PNG")

        return response
    else:
        image = Image.open(photo.image.path)
        w, h = image.size
        image = image.resize((w // 2, h // 2))

        response = HttpResponse(content_type="image/png")
        image.save(response, "PNG")

        return response

        #
        # with open(photo.image.path, "rb") as f:
        #    return HttpResponse(f.read(), content_type="image/png")


def get_index_detail(request):
    map_count = LMMap.objects.count()
    place_count = LMPlace.objects.filter(user__isnull=False).count()

    place_photo = LMPlace.objects.annotate(num_photos=Count('photos')).filter(user__isnull=False, display__exact=True,
                                                                              num_photos__gt=0).all()[:10]
    # place_photo = [h.as_detail() for h in list(place_photo)]
    place_photo = random.choice(list(place_photo))
    place_photo = place_photo.as_detail()

    return JsonResponse(dict(place_photo=place_photo, map_count=map_count, place_count=place_count))
