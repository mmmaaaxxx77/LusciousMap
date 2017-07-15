# coding=utf-8
import os
import uuid

import googlemaps
import requests
from django.contrib.auth.decorators import login_required
from django.core.files import File
from django.db.models import Q, Count
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse

from LusciousMap import settings
from frontend.google_service.views import service_key_getter
from frontend.map_basic.form import ImageUploadForm
from frontend.map_basic.models import LMPlaceType, LMCountry, LMCity, LMAttraction, LMPlace, LMRating, LMPhoto, LMTag
from frontend.map_map.models import LMMapPlace, LMUserDetail, LMMap

import urllib.request
from PIL import Image


def search_place(request):
    if request.method == 'GET':
        search_str = request.GET["term"]

        result = []
        search_place = LMPlace.objects.filter(Q(user__isnull=False) &
                                              Q(display__exact=True) &
                                              (Q(name__contains=search_str) |
                                               Q(description__contains=search_str) |
                                               Q(tags__name__contains=search_str))).annotate(dcount=Count('name')).all()[:10]

        result.extend([h.as_search_json_view() for h in list(search_place)])
        return JsonResponse(result, safe=False)


def search_tag(request):
    if request.method == 'GET':
        search_str = request.GET["term"]

        search_tags = LMTag.objects.filter(name__contains=search_str)
        result = []
        result.extend([h.name for h in list(search_tags)])

        return JsonResponse(result, safe=False)


def new_place(request):
    if request.method == 'POST':
        save_new_place(request)
        return HttpResponseRedirect(reverse('index'))


def save_new_place(request):
    # check
    if request.POST['name'].encode('utf-8').strip() == '' or \
                    request.POST['geo_lat'] is None or \
                    request.POST['geo_lng'] is None or \
                    request.POST['place_id'] is None:
        return HttpResponseRedirect(reverse('index'))

    photo = None
    form = ImageUploadForm(request.POST, request.FILES)
    if form.is_valid():
        photo = LMPhoto()
        photo.image = request.FILES['picture']
        photo.save()

    post_place_id = request.POST['place_id']
    place = LMPlace.objects.filter(google_place_id__exact=post_place_id).all()
    if len(list(place)) == 0:
        place = createLMPlace(request, photo)
    else:
        place = place[0]
        if photo is not None:
            place.photos.add(photo)
            place.save()

    if not request.user.is_authenticated:
        return place

    map_place = LMMapPlace() if LMMapPlace.objects.filter(place_id__exact=place.id).count() == 0 else LMMapPlace.objects.filter(place__exact=place).all()[0]
    map_place.place = place
    map_place.name = request.POST['name'].encode('utf-8')
    map_place.save()
    if not request.user.is_authenticated:
        map_place.display = False
    map_place.description = request.POST['description'].encode('utf-8')
    if photo is not None:
        map_place.photos.add(photo)
    # map_father_id ?

    # tags
    tags_s = request.POST['tags']
    if len(tags_s) != 0:
        tags_s = tags_s.split(",")
        map_place.tags.clear()
        for tag in tags_s:
            try:
                tag_inst = LMTag.objects.get(name__exact=tag)
            except:
                tag_inst = LMTag()
                tag_inst.name = tag
                tag_inst.save()
                tag_inst.createUser = request.user
            map_place.tags.add(tag_inst)

    # auth
    if request.user.is_authenticated:
        map_place.user = request.user

    map_place.save()

    # user detail
    if request.user.is_authenticated:
        detail = LMUserDetail.objects.get(user_id__exact=request.user.id)
        detail.my_place.add(map_place)
        detail.save()

    return map_place


def createLMPlace(request, photo):
    # gmap
    language = request.LANGUAGE_CODE
    gmaps = googlemaps.Client(key=service_key_getter(1))
    result = gmaps.place(request.POST['place_id'], language=language)

    # gmap static image
    url = "https://maps.googleapis.com/maps/api/staticmap?scale=2&zoom=18&size=500x500&maptype=roadmap"
    url += "&center={},{}".format(request.POST['geo_lat'], request.POST['geo_lng'])
    url += "&markers=color:red%7C{},{}".format(request.POST['geo_lat'], request.POST['geo_lng'])
    url += "&key={}".format(service_key_getter(1))

    filename = "{}.png".format(uuid.uuid4())
    map_image_path = settings.MEDIA_ROOT + "/map_images/" + filename

    r = urllib.request.urlretrieve(url, map_image_path)
    map_image = LMPhoto()
    map_image.image.save(filename, File(open(map_image_path,'rb')))
    map_image.save()

    if os.path.isfile(map_image_path):
        os.remove(map_image_path)

    # place
    place = LMPlace()

    place.map_image = map_image

    place.name = request.POST['name'].encode('utf-8').strip()
    place.description = request.POST['description'].encode('utf-8')
    typee = LMPlaceType.objects.filter(id__exact=request.POST['type'])[0]
    place.place_type = typee
    country = LMCountry.objects.filter(id__exact=request.POST['country'])[0]
    place.country = country
    """
    if request.POST['city'] != 'null':
        city = LMCity.objects.filter(id__exact=request.POST['city'])[0]
        place.city = city
    if request.POST['attraction'] != 'null':
        attraction = LMAttraction.objects.filter(id__exact=request.POST['attraction'])[0]
        place.attraction = attraction
    """

    place.geo_lat = request.POST['geo_lat']
    place.geo_lng = request.POST['geo_lng']
    rating = LMRating()
    place.rating = rating
    rating.save()
    place.save()

    # auth
    if request.user.is_authenticated:
        place.user = request.user

    # tags
    tags_s = request.POST['tags']
    if len(tags_s) != 0:
        tags_s = tags_s.split(",")
        place.tags.clear()
        for tag in tags_s:
            tag_inst = LMTag.objects.filter(name__exact=tag).all()
            if len(tag_inst) != 0:
                tag_inst = tag_inst[0]
            else:
                tag_inst = LMTag()
                tag_inst.name = tag
                tag_inst.save()
                if request.user.is_authenticated:
                    tag_inst.createUser = request.user
            place.tags.add(tag_inst)

    # photo
    #if photo is not None:
    #    place.photos.add(photo)

    # google
    place.google_place_id = request.POST['place_id']
    if result['status'] == 'OK':
        try:
            place.google_rating = float(result['result']['rating']) if "rating" in result['result'].keys() else 0
            place.google_id = result['result']['id'] if "id" in result['result'].keys() else ""
            place.google_map_url = result['result']['url'] if "url" in result['result'].keys() else ""
            place.google_website = result['result']['website'] if "website" in result['result'].keys() else ""
            place.google_phone_number = result['result']['formatted_phone_number'] if "formatted_phone_number" in result['result'].keys() else ""
            place.google_international_phone_number = result['result']['international_phone_number'] if "international_phone_number" in result['result'].keys() else ""
            place.google_address = result['result']['formatted_address'] if "formatted_address" in result['result'].keys() else ""
            place.name = result['result']['name'] if "name" in result['result'].keys() else ""
        except:
            print("{} google fail.".format(place.id))

    g_photos = result['result']['photos'] if "photos" in result['result'].keys() else []
    for photo in g_photos:
        photo_obj = get_google_photo(photo["width"], photo["height"], photo['photo_reference'])
        place.photos.add(photo_obj)

    rating.save()
    place.save()

    return place


def get_google_photo(width, height, photo_reference):
    url = "https://maps.googleapis.com/maps/api/place/photo?sensor=false&key={}".format(service_key_getter(1))
    url += "&photoreference={}".format(photo_reference)
    url += "&maxheight={}&maxwidth={}".format(height, width)

    filename = "{}.png".format(uuid.uuid4())
    map_image_path = settings.MEDIA_ROOT + "/map_images/" + filename

    r = urllib.request.urlretrieve(url, map_image_path)

    small_photo = Image.open(map_image_path)
    w, h = small_photo.size
    if w >= 1600 or h>= 1600:
        small_photo = small_photo.resize((w // 2, h // 2))
        small_photo.save(map_image_path, "PNG")

    map_image = LMPhoto()
    map_image.image.save(filename, File(open(map_image_path, 'rb')))
    map_image.save()

    if os.path.isfile(map_image_path):
        os.remove(map_image_path)

    return map_image


@login_required
def good_to_place(request, place_id):
    if request.user.is_authenticated:
        user = request.user
        place = LMPlace.objects.get(id__exact=place_id)

        # 檢查bad
        if user in place.rating.bad.all():
            place.rating.bad.remove(user)

        if user in place.rating.good.all():
            return JsonResponse(dict(auth=True, success=False))
        else:
            place.rating.good.add(user)
            return JsonResponse(dict(auth=True, success=True))
    else:
        return JsonResponse(dict(auth=False, success=False))


@login_required
def bad_to_place(request, place_id):
    if request.user.is_authenticated:
        user = request.user
        place = LMPlace.objects.get(id__exact=place_id)

        # 檢查good
        if user in place.rating.good.all():
            place.rating.good.remove(user)

        if user in place.rating.bad.all():
            return JsonResponse(dict(auth=True, success=False))
        else:
            place.rating.bad.add(user)
            return JsonResponse(dict(auth=True, success=True))
    else:
        return JsonResponse(dict(auth=False, success=False))


def place_detail(request, place_id):
    try:
        place = LMPlace.objects.get(id__exact=place_id)
        place_json = place.as_detail()
    except:
        place = LMMapPlace.objects.get(id__exact=place_id)
        place_json = place.place.as_detail()
        place_json['name'] = place.name
        place_json['description'] = place.description
        place_json['photos'] = place.as_detail()['photos']

    return JsonResponse(dict(place=place_json))
