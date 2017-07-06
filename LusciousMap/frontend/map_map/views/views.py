import random

from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.http import JsonResponse
from django.shortcuts import render

from LusciousMap.core.paging.CusPaginator import setUpPagingObjects, generatePagingJSONResult, setUpPagingObjectsJson
from frontend.map_basic.models import LMPlace
from frontend.map_map.models import LMMapPlace, LMMap


def search_place(request):
    if request.method == 'GET':
        search_str = request.GET["term"]

        result = []
        search_place = LMPlace.objects.filter(Q(user__isnull=False) &
                                              Q(display__exact=True) &
                                              (Q(name__contains=search_str) |
                                               Q(description__contains=search_str) |
                                               Q(tags__name__contains=search_str))).annotate(dcount=Count('name')).all()[:10]
        search_mapplace = LMMapPlace.objects.filter(Q(user__isnull=False) &
                                                    Q(display__exact=True) &
                                                    (Q(name__contains=search_str) |
                                                     Q(description__contains=search_str) |
                                                     Q(tags__name__contains=search_str))).annotate(dcount=Count('name')).all()[:10]
        search_mapmap = LMMap.objects.filter(Q(user__isnull=False) &
                                             Q(display__exact=True) &
                                             (Q(name__contains=search_str) |
                                              Q(description__contains=search_str) |
                                              Q(tags__name__contains=search_str))).annotate(dcount=Count('name')).all()[:10]

        result.extend([h.as_search_json() for h in list(search_place)])
        result.extend([h.as_search_json() for h in list(search_mapplace)])
        result.extend([h.as_search_json() for h in list(search_mapmap)])
        random.shuffle(result)
        return JsonResponse(result, safe=False)


def search_place_list(request):
    if request.method == 'GET':
        search_str = request.GET["term"]

        if len(search_str) == 0 or search_str is None:
            return init_recommend_list(request)

        result = []
        search_place = LMPlace.objects.filter(Q(user__isnull=False) &
                                              Q(display__exact=True) &
                                              (Q(name__contains=search_str) |
                                               Q(description__contains=search_str) |
                                               Q(tags__name__contains=search_str))).annotate(dcount=Count('name')).all()
        """
        search_mapplace = LMMapPlace.objects.filter(Q(user__isnull=False) &
                                                    Q(display__exact=True) &
                                                    (Q(name__contains=search_str) |
                                                     Q(description__contains=search_str) |
                                                     Q(tags__name__contains=search_str))).annotate(dcount=Count('name')).all()
        """
        search_mapmap = LMMap.objects.filter(Q(user__isnull=False) &
                                             Q(display__exact=True) &
                                             (Q(name__contains=search_str) |
                                              Q(description__contains=search_str) |
                                              Q(tags__name__contains=search_str))).annotate(dcount=Count('name')).all()

        result.extend([h.as_detail() for h in list(search_place)])
        #result.extend([h.as_detail() for h in list(search_mapplace)])
        result.extend([h.as_detail() for h in list(search_mapmap)])
        #random.shuffle(result)
        result = sorted(result, key=lambda place: place['rating']['good'], reverse=True)
        page = request.GET["page"] if "page" in request.GET.keys() else 1
        size = request.GET["size"] if "size" in request.GET.keys() else 8

        res = setUpPagingObjectsJson(page=page, size=size, objects=result)

        return generatePagingJSONResult(pagingObject=res, SerializerObject=res['result'])


def init_recommend_list(request):
    if request.method == 'GET':
        result = []
        search_place = LMPlace.objects.filter(Q(user__isnull=False) & Q(display__exact=True)).annotate(dcount=Count("name")).all()
        """
        search_mapplace = LMMapPlace.objects.filter(user__isnull=False, display__exact=True).order_by(
            "-place__rating__good")
        """
        search_mapmap = LMMap.objects.filter(Q(user__isnull=False) & Q(display__exact=True)).annotate(dcount=Count('name')).all()

        list_search_place = [h.as_detail() for h in list(search_place)]
        #list_search_mapplace = [h.as_detail() for h in list(search_mapplace)]
        list_search_mapmap = [h.as_detail() for h in list(search_mapmap)]

        result.extend(list_search_place)
        #result.extend(list_search_mapplace)
        result.extend(list_search_mapmap)
        #random.shuffle(result)
        result = sorted(result, key=lambda place: place['rating']['good'], reverse=True)
        page = request.GET["page"] if "page" in request.GET.keys() else 1
        size = request.GET["size"] if "size" in request.GET.keys() else 8

        res = setUpPagingObjectsJson(page=page, size=size, objects=result)

        return generatePagingJSONResult(pagingObject=res, SerializerObject=res['result'])


@login_required
def good_to_map(request, place_id):
    if request.user.is_authenticated:
        user = request.user
        place = LMMap.objects.get(id__exact=place_id)

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
def bad_to_map(request, place_id):
    if request.user.is_authenticated:
        user = request.user
        place = LMMap.objects.get(id__exact=place_id)

        # 檢查bad
        if user in place.rating.good.all():
            place.rating.good.remove(user)

        if user in place.rating.bad.all():
            return JsonResponse(dict(auth=True, success=False))
        else:
            place.rating.bad.add(user)
        return JsonResponse(dict(auth=True, success=True))
    else:
        return JsonResponse(dict(auth=False, success=False))
