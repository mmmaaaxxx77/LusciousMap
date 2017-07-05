import os
import urllib.request
import uuid

from django.contrib.auth.decorators import login_required
from django.core.files import File
from django.http import JsonResponse
from django.shortcuts import render

from LusciousMap import settings
from frontend.google_service.views import service_key_getter
from frontend.map_basic.form import MapUploadForm, ImageUploadForm
from frontend.map_basic.models import LMPlaceType, LMCountry, LMRating, LMTag, LMPhoto, LMPlace
from frontend.map_basic.views import save_new_place
from frontend.map_map.models import LMMap, LMMapPlace, LMUserDetail


@login_required
def list_follows(request):
    user = request.user
    detail = LMUserDetail.objects.get(user__exact=user)
    follows = detail.my_follow.filter(display__exact=True).all()
    follows = [follow.as_detail() for follow in follows]
    return JsonResponse(dict(follows=follows))


@login_required
def list_mapplace(request):
    user = request.user
    places = LMMapPlace.objects.filter(user__exact=user, display__exact=True).order_by("-createDate").all()

    places = [place.as_detail() for place in places]

    return JsonResponse(dict(places=places))


def detail_mapplace(request, place_id):
    place = LMMapPlace.objects.get(id__exact=place_id)

    return JsonResponse(dict(place=place.as_detail()))


@login_required
def list_map(request):
    user = request.user
    maps = LMMap.objects.filter(user__exact=user, display__exact=True).order_by("-createDate").all()

    maps = [map.as_detail() for map in maps]

    return JsonResponse(dict(maps=maps))


def detail_map(request, map_id):
    map = LMMap.objects.get(id__exact=map_id)
    return JsonResponse(dict(map=map.as_detail()))


@login_required
def edit_map(request):
    if request.method == 'GET':
        # type
        types = LMPlaceType.objects.order_by("createDate").all()
        # 國家
        countries = LMCountry.objects.order_by("createDate").all()

        form_options = {
            "types": [typee.as_json() for typee in types],
            "countries": [country.as_json() for country in countries],
        }

        return JsonResponse(form_options)
    elif request.method == 'POST':
        save_map(request)
        return JsonResponse(dict(success=True))


@login_required
def save_map(request):

    user = request.user
    print(request.POST['map_id'])
    if len(request.POST['map_id']) != 0:
        print("edit map")
        map = LMMap.objects.get(id__exact=request.POST['map_id'])
        map.name = request.POST['map_name']
        map.description = request.POST['map_description'] if 'map_description' in request.POST.keys() else ""
        map.save()
        # type
        p_type = LMPlaceType.objects.filter(id__exact=request.POST['map_type']).all()[0]
        map.place_types.clear()
        map.place_types.add(p_type)
        # country
        p_country = LMCountry.objects.filter(id__exact=request.POST['map_country']).all()[0]
        map.countries.clear()
        map.countries.add(p_country)
        # tags
        tags_s = request.POST['map_tags']
        tags_s = tags_s.split(",")
        map.tags.clear()
        if len(tags_s) != 0:
            for tag in tags_s:
                try:
                    tag_inst = LMTag.objects.get(name__exact=tag)
                except:
                    tag_inst = LMTag()
                    tag_inst.name = tag
                    tag_inst.save()
                    tag_inst.createUser = request.user
                map.tags.add(tag_inst)
        # photo
        photo = None
        form = MapUploadForm(request.POST, request.FILES)
        if form.is_valid():
            print("yes photo")
            photo = LMPhoto()
            photo.image = request.FILES['map_picture']
            photo.save()
            map.photos.add(photo)
        map.save()
        pass
    else:
        print("new map")
        # new
        map = LMMap()
        map.name = request.POST['map_name']
        map.description = request.POST['map_description'] if 'map_description' in request.POST.keys() else ""
        map.save()
        # user
        map.user = user
        # type
        p_type = LMPlaceType.objects.filter(id__exact=request.POST['map_type']).all()[0]
        map.place_types.add(p_type)
        # country
        p_country = LMCountry.objects.filter(id__exact=request.POST['map_country']).all()[0]
        map.countries.add(p_country)
        # rating
        rating = LMRating()
        rating.save()
        map.rating = rating
        map.save()
        # tags
        tags_s = request.POST['map_tags']
        tags_s = tags_s.split(",")
        map.tags.clear()
        if len(tags_s) != 0:
            for tag in tags_s:
                try:
                    tag_inst = LMTag.objects.get(name__exact=tag)
                except:
                    tag_inst = LMTag()
                    tag_inst.name = tag
                    tag_inst.save()
                    tag_inst.createUser = request.user
                map.tags.add(tag_inst)
        # photo
        photo = None
        form = MapUploadForm(request.POST, request.FILES)
        if form.is_valid():
            print("yes photo")
            photo = LMPhoto()
            photo.image = request.FILES['map_picture']
            photo.save()
            map.photos.add(photo)
        # static map photo
        map.map_image = get_static_map_photo(23.9037, 121.0794, 10)
        map.save()

        # user detail
        if request.user.is_authenticated:
            detail = LMUserDetail.objects.get(user_id__exact=request.user.id)
            detail.my_maps.add(map)
            detail.save()


def get_static_map_photo(geo_lat, geo_lng, zoom):
    # gmap static image
    url = "https://maps.googleapis.com/maps/api/staticmap?scale=2&zoom={}&size=500x500&maptype=roadmap".format(zoom)
    url += "&center={},{}".format(geo_lat, geo_lng)
    url += "&markers=color:red%7C{},{}".format(geo_lat, geo_lng)
    url += "&key={}".format(service_key_getter(1))

    filename = "{}.png".format(uuid.uuid4())
    map_image_path = settings.MEDIA_ROOT + "/map_images/" + filename

    r = urllib.request.urlretrieve(url, map_image_path)
    map_image = LMPhoto()
    map_image.image.save(filename, File(open(map_image_path,'rb')))
    map_image.save()

    if os.path.isfile(map_image_path):
        os.remove(map_image_path)

    return map_image


@login_required
def save_map_mark(request):
    if request.method == 'POST':
        user = request.user
        # 地圖新增地點
        if len(request.POST['map_id']) > 0 and len(request.POST['edit_place_id']) == 0:
            map_id = request.POST['map_id']
            map = LMMap.objects.get(id__exact=map_id, user__exact=user)
            place = save_new_place(request)
            if map.places.filter(place_id__exact=place.id).count() == 0:
                map.places.add(place)
            if map.places.count() > 0:
                image = get_map_static_image(map.places.all())
                try:
                    map.map_image.delete()
                    map.save()
                except:
                    print("delete image error")
                map.map_image = image

            map.save()
            return JsonResponse(dict(success=True))
        # 地點新增地點
        elif len(request.POST['map_id']) == 0 and len(request.POST['edit_place_id']) == 0:
            place = save_new_place(request)
            return JsonResponse(dict(success=True))
        # 修改地圖地點
        elif len(request.POST['map_id']) > 0 and len(request.POST['edit_place_id']) > 0:
            place = LMMapPlace.objects.get(id__exact=request.POST['edit_place_id'], user__exact=user)
            edit_map_place(request, place)
            return JsonResponse(dict(success=True))
            pass
        # 修改地點的地點
        elif len(request.POST['map_id']) == 0 and len(request.POST['edit_place_id']) > 0:
            place = LMMapPlace.objects.get(id__exact=request.POST['edit_place_id'], user__exact=user)
            edit_map_place(request, place)
            return JsonResponse(dict(success=True))
            pass

        return JsonResponse(dict(success=False))


@login_required
def edit_map_place(request, place):
    place.name = request.POST['name']
    place.description = request.POST['description']
    tags_s = request.POST['tags']
    if len(tags_s) != 0:
        tags_s = tags_s.split(",")
        place.tags.clear()
        for tag in tags_s:
            try:
                tag_inst = LMTag.objects.get(name__exact=tag)
            except:
                tag_inst = LMTag()
                tag_inst.name = tag
                tag_inst.save()
                tag_inst.createUser = request.user
            place.tags.add(tag_inst)

    photo = None
    form = ImageUploadForm(request.POST, request.FILES)
    if form.is_valid():
        photo = LMPhoto()
        photo.image = request.FILES['picture']
        photo.save()
        place.photos.add(photo)
    place.save()
    return place


def get_map_static_image(geo_list):
    # gmap static image
    url = "https://maps.googleapis.com/maps/api/staticmap?scale=2&zoom=14&size=500x500&maptype=roadmap"
    url += "&center={},{}".format(geo_list[0].place.geo_lat, geo_list[0].place.geo_lng)
    for geo in geo_list:
        url += "&markers=color:blue%7C{},{}".format(geo.place.geo_lat, geo.place.geo_lng)
    url += "&key={}".format(service_key_getter(1))

    filename = "{}.png".format(uuid.uuid4())
    map_image_path = settings.MEDIA_ROOT + "/map_images/" + filename

    r = urllib.request.urlretrieve(url, map_image_path)
    map_image = LMPhoto()
    map_image.image.save(filename, File(open(map_image_path,'rb')))
    map_image.save()

    if os.path.isfile(map_image_path):
        os.remove(map_image_path)

    return map_image
