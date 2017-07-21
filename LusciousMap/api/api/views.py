import os
import urllib.request
import uuid

import googlemaps
from django.contrib.auth.models import User
from django.core.files import File
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from LusciousMap import settings
from frontend.google_service.views import service_key_getter
from frontend.leaderboard.models import LBPlace, LBTopic
from frontend.map_basic.models import LMPlaceType, LMCountry, LMPlace, LMRating, LMPhoto, LMTag

API_KEY = ["ABCDEFG"]


@csrf_exempt
def new_lbplace(request):
    if request.method == 'POST':
        if request.POST['token'] in API_KEY:
            return save_lbplace(request)
        return HttpResponseForbidden()


def save_lbplace(request):
    try:
        places = LBPlace.objects.filter(place__google_place_id__exact=request.POST['place_id'])
        if len(places) > 0:
            place = places[0]
            place.rating_good_score = request.POST['rating_good_score']
            place.save()

            topic = LBTopic.objects.get(id__exact=request.POST['topic_id'])
            if place not in topic.places.all():
                topic.places.add(place)
                topic.save()
            return HttpResponse("edit ok")
        else:
            place_id = request.POST['place_id']
            rating_good_score = request.POST['rating_good_score']
            rating_bad_score = 0
            lmplace = LMPlace.objects.get(google_place_id__exact=place_id)
            lbplace = LBPlace()
            lbplace.place = lmplace
            lbplace.rating_good_score = rating_good_score
            lbplace.save()

            topic = LBTopic.objects.get(id__exact=request.POST['topic_id'])
            topic.places.add(lbplace)
            topic.save()

            return HttpResponse("ok")

    except Exception as e:
        print("{}".format(e))
        return HttpResponse("{}".format(e))



@csrf_exempt
def new_place(request):
    if request.method == 'POST':
        print(request.POST['token'])
        if request.POST['token'] in API_KEY:
            print(request.POST)
            return save_new_place(request)
        return HttpResponseForbidden()


def save_new_place(request):
    # check
    print(request.POST)
    if request.POST['geo_lat'] is None or \
                    request.POST['geo_lng'] is None or \
                    request.POST['place_id'] is None:
        return HttpResponseForbidden()

    post_place_id = request.POST['place_id']
    place = LMPlace.objects.filter(google_place_id__exact=post_place_id).all()
    if len(list(place)) == 0:
        return createLMPlace(request)

    return HttpResponse("already exists")


def createLMPlace(request):
    g_photos_result = []
    try:
        # gmap
        language = request.LANGUAGE_CODE
        gmaps = googlemaps.Client(key=service_key_getter(1))
        result = gmaps.place(request.POST['place_id'], language=language)

        # gmap static image
        url = "https://maps.googleapis.com/maps/api/staticmap?scale=2&zoom=18&size=500x500&maptype=roadmap"
        url += "&center={},{}".format(request.POST['geo_lat'], request.POST['geo_lng'])
        url += "&markers=color:red%7C{},{}".format(request.POST['geo_lat'], request.POST['geo_lng'])
        url += "&key={}".format("AIzaSyDhejmQaWv0GJqAgs7m0twK4tylUepgYgA")

        filename = "{}.png".format(uuid.uuid4())
        map_image_path = settings.MEDIA_ROOT + "/map_images/" + filename

        r = urllib.request.urlretrieve(url, map_image_path)

        # get google photo
        g_photos = result['result']['photos'] if "photos" in result['result'].keys() else []
        for photo in g_photos:
            photo_obj = get_google_photo(photo["width"], photo["height"], photo['photo_reference'])
            g_photos_result.append(photo_obj)

    except Exception as e:
        for photo in g_photos_result:
            photo.delete()

        return HttpResponse("{}".format(e))

    map_image = LMPhoto()
    map_image.image.save(filename, File(open(map_image_path, 'rb')))
    map_image.save()

    if os.path.isfile(map_image_path):
        os.remove(map_image_path)

    # place
    place = LMPlace()

    place.map_image = map_image

    place.name = result['result']['name'].strip()
    #place.description = request.POST['description'].encode('utf-8')
    place.description = ""
    typee = LMPlaceType.objects.filter(id__exact=request.POST['type']).all()[0]
    place.place_type = typee
    country = LMCountry.objects.filter(id__exact=request.POST['country']).all()[0]
    place.country = country

    place.geo_lat = request.POST['geo_lat']
    place.geo_lng = request.POST['geo_lng']
    rating = LMRating()
    place.rating = rating
    rating.save()
    place.save()

    # tags
    """
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
    """

    # google
    place.google_place_id = request.POST['place_id']
    if result['status'] == 'OK':
        try:
            place.opening_hours_weekday_text = "\r\n".join(result['result']['opening_hours']['weekday_text'])
        except Exception as e:
            print("cannot find opening hours")
            print("{}".format(e))

        try:
            place.google_rating = float(result['result']['rating']) if "rating" in result['result'].keys() else 0
            place.google_id = result['result']['id'] if "id" in result['result'].keys() else ""
            place.google_map_url = result['result']['url'] if "url" in result['result'].keys() else ""
            place.google_website = result['result']['website'] if "website" in result['result'].keys() else ""
            place.google_phone_number = result['result']['formatted_phone_number'] if "formatted_phone_number" in \
                                                                                      result['result'].keys() else ""
            place.google_international_phone_number = result['result'][
                'international_phone_number'] if "international_phone_number" in result['result'].keys() else ""
            place.google_address = result['result']['formatted_address'] if "formatted_address" in result[
                'result'].keys() else ""
            place.name = result['result']['name'] if "name" in result['result'].keys() else ""
        except:
            print("{} google fail.".format(place.id))

    for photo in g_photos_result:
        place.photos.add(photo)

    try:
        user = User.objects.get(username__exact="johnny")
        place.user = user
    except Exception as e:
        print("{}".format(e))

    rating.save()
    place.save()

    return HttpResponse("ok")


def get_google_photo(width, height, photo_reference):
    url = "https://maps.googleapis.com/maps/api/place/photo?sensor=false&key={}".format("AIzaSyCJj1F_97Me7yqQ0avkPAxptm-Vic_a4-Y")
    url += "&photoreference={}".format(photo_reference)
    url += "&maxheight={}&maxwidth={}".format(height, width)

    filename = "{}.png".format(uuid.uuid4())
    map_image_path = settings.MEDIA_ROOT + "/map_images/" + filename

    r = urllib.request.urlretrieve(url, map_image_path)
    map_image = LMPhoto()
    map_image.image.save(filename, File(open(map_image_path, 'rb')))
    map_image.save()

    if os.path.isfile(map_image_path):
        os.remove(map_image_path)

    return map_image
