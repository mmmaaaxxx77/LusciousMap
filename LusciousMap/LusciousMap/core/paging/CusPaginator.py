from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.http import JsonResponse

__author__ = 'johnnytsai'


def setUpPagingObjectsJson(objects, page, size, **dic):

    # paging
    paginator = Paginator(objects, size)
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
        page = 1
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    data = [ob for ob in objects.object_list]

    return dict(result=data, page=page, totalPages=paginator.num_pages, totalResults=paginator.count)


def setUpPagingObjects(objects, page, size, **dic):

    # paging
    paginator = Paginator(objects, size)
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
        page = 1
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    data = [ob.as_json() for ob in objects.object_list]

    return dict(result=data, page=page, totalPages=paginator.num_pages, totalResults=paginator.count)


def setUpPagingObject(object, page, size, **dic):
    # filter
    if 'filter' in dic and dic['filter'] is not None:
        objects = object.objects.filter(**dic['filter'])
    else:
        objects = object.objects.all()

    # sort
    if 'sort' in dic and dic['sort'] is not None:
        objects = objects.extra(order_by=[dic['sort']])

    # paging
    paginator = Paginator(objects, size)
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
        page = 1
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return dict(result=objects, page=page, totalPages=paginator.num_pages, totalResults=paginator.count)


def generatePagingJSONResult(pagingObject, SerializerObject):
    return JsonResponse(dict(success=True, result=SerializerObject, page=pagingObject['page'], totalPages=pagingObject['totalPages'], totalResults=pagingObject['totalResults']))
