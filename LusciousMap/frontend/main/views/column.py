import random

from django.db.models import Q, Count
from django.http import JsonResponse
from django.shortcuts import render

from frontend.column.models import LMColumn
from frontend.map_basic.models import LMTag


def index(request):
    tmp = []
    count = LMColumn.objects.count()
    if count == 0:
        return render(request, "column/index.html", dict(tags=[]))
    for ob in LMColumn.objects.all():
        tmp = set(tmp).union(ob.tags.all())

    tags = random.sample(tmp, 5)
    return render(request, "column/index.html", dict(tags=list(tags)))


def detail(request, column_id):
    count = LMColumn.objects.count()
    if count == 0:
        return render(request, "column/detail.html", dict(column=[],
                                                          recommend_columns=[]))

    recommend_columns = random.sample(list(LMColumn.objects.filter(display__exact=True).all()), count if count < 5 else 5)
    column = LMColumn.objects.get(id__exact=column_id)

    return render(request, "column/detail.html", dict(column=column,
                                                      recommend_columns=recommend_columns))


def search_column(request):
    if request.method == 'GET':

        if "term" in request.GET.keys():
            search_str = request.GET["term"]
            print(search_str)
            if len(search_str) == 0 or search_str is None:
                return init_recommend_list(request)
        else:
            return init_recommend_list(request)

        page = int(request.GET["page"]) if "page" in request.GET.keys() else 1
        size = int(request.GET["size"]) if "size" in request.GET.keys() else 5

        count = LMColumn.objects.count()
        total_page_size = int(count/size)
        if count % size != 0:
            total_page_size += 1

        start = (page-1)*size
        if start > total_page_size:
            start = total_page_size
        end = start+size
        columns = LMColumn.objects.filter(Q(display__exact=True) & (Q(title__contains=search_str) |
                                                                    Q(tags__name__contains=search_str) |
                                                                    Q(content__contains=search_str) |
                                                                    Q(short_description__contains=search_str))) \
                      .annotate(dcount=Count('title')).order_by("-updateDate").all()[start:end]

        columns = [c.as_json() for c in columns]

        return JsonResponse(dict(columns=columns, total=len(columns), page=page, size=size))


def init_recommend_list(request):
    if request.method == 'GET':
        page = int(request.GET["page"]) if "page" in request.GET.keys() else 1
        size = int(request.GET["size"]) if "size" in request.GET.keys() else 5

        count = LMColumn.objects.count()
        total_page_size = int(count/size)
        if count % size != 0:
            total_page_size += 1

        start = (page-1)*size
        if start > total_page_size:
            start = total_page_size
        end = start+size

        result = []
        columns = LMColumn.objects.filter(display__exact=True).order_by("-updateDate").all()[start:end]

        columns = [c.as_json() for c in columns]

        return JsonResponse(dict(columns=columns, total=len(columns), page=page, size=size))


def recommend_column(request):
    columns = random.sample(list(LMColumn.objects.all()), 1)
    return JsonResponse(dict(columns=columns, self=False))
