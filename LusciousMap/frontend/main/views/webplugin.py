from django.shortcuts import render
from django.urls import reverse

from frontend.map_basic.models import LMPlace
from frontend.map_map.models import LMMap


def map(request, map_id):
    map = LMMap.objects.get(id__exact=map_id)
    return render(request, "webplugin/map.html", dict(map=map))


def place(request, place_id):
    place = LMPlace.objects.get(id__exact=place_id)

    return render(request, "webplugin/place.html", dict(place=place))


def map_view(request, map_id):
    return render(request, "place/map_view.html", dict(map=dict(id=map_id,
                                                                url=reverse('detail_map', args=[map_id]))))
