import datetime
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect, csrf_exempt

from frontend.leaderboard.models import LBTopic, LBComment, LBPlace


def index(request):
    topics = LBTopic.objects.filter(display__exact=True).all()
    return render(request, "leaderboard/index.html", dict(topics=topics))


def detail(request, topic_id):
    topic = LBTopic.objects.get(id__exact=topic_id)
    return render(request, "leaderboard/detail.html", dict(topic=topic))


def get_topic(request, topic_id):
    topic = LBTopic.objects.get(id__exact=topic_id)
    return JsonResponse(dict(topic=topic))


def get_g_places(request, topic_id):

    page = int(request.GET["page"]) if "page" in request.GET.keys() else 1
    size = int(request.GET["size"]) if "size" in request.GET.keys() else 10

    topic = LBTopic.objects.get(id__exact=topic_id)

    places_obj = topic.places

    count = places_obj.count()
    total_page_size = int(count / size)
    if count % size != 0:
        total_page_size += 1

    start = (page - 1) * size
    if start > total_page_size:
        start = total_page_size
    end = start + size

    if "term" in request.GET.keys():
        search_str = request.GET["term"]
        if len(search_str) == 0 or search_str is None:
            places = places_obj
        else:
            places = places_obj.filter(place__name__contains=search_str)
    else:
        places = places_obj

    places = places.order_by("-rating_good_score").all()[start:end]

    return JsonResponse(dict(
        places=[t.to_detail() for t in places],
        page=page,
        total=total_page_size,
    ))


def get_b_places(request, topic_id):
    page = int(request.GET["page"]) if "page" in request.GET.keys() else 1
    size = int(request.GET["size"]) if "size" in request.GET.keys() else 10

    topic = LBTopic.objects.get(id__exact=topic_id)

    places_obj = topic.places

    count = places_obj.count()
    total_page_size = int(count / size)
    if count % size != 0:
        total_page_size += 1

    start = (page - 1) * size
    if start > total_page_size:
        start = total_page_size
    end = start + size

    if "term" in request.GET.keys():
        search_str = request.GET["term"]
        if len(search_str) == 0 or search_str is None:
            places = places_obj
        else:
            places = places_obj.filter(place__name__contains=search_str)
    else:
        places = places_obj

    places = places.order_by("-rating_bad_score").all()[start:end]

    return JsonResponse(dict(
        places=[t.to_detail() for t in places],
        page=page,
        total=total_page_size,
    ))


def search_places(request, topic_id):

    if "term" in request.GET.keys():
        search_str = request.GET["term"]
        topic = LBTopic.objects.get(id__exact=topic_id)
        places = topic.places.filter(place__name__contains=search_str).all()
        return JsonResponse(dict(places=[t.place.as_detail() for t in places]))
    else:
        return JsonResponse(dict(places=[]))


@login_required
@csrf_exempt
def save_g_comment(request, place_id):
    place = LBPlace.objects.get(id__exact=place_id)

    if 'comment_id' not in request.POST.keys():
        comment = LBComment()
        comment.comment = request.POST['comment_text']
        comment.user = request.user
        comment.save()
        place.positive_comment.add(comment)
        place.save()
    else:
        comment_id = request.POST['comment_id']
        comment = LBComment.objects.filter(id__exact=comment_id).all()
        comment_obj = comment[0]
        now = datetime.datetime.now().isoformat()
        comment_obj.comment = "{}\n<<<{}>>>\n{}".format(comment_obj.comment, now, request.POST['comment_text'])
        comment_obj.save()

    return JsonResponse(dict(success=True))


@login_required
@csrf_exempt
def save_b_comment(request, place_id):
    place = LBPlace.objects.get(id__exact=place_id)

    if 'comment_id' not in request.POST.keys():
        comment = LBComment()
        comment.comment = request.POST['comment_text']
        comment.user = request.user
        comment.save()
        place.negative_comment.add(comment)
        place.save()
    else:
        comment_id = request.POST['comment_id']
        comment = LBComment.objects.filter(id__exact=comment_id).all()
        comment_obj = comment[0]
        now = datetime.datetime.now().isoformat()
        comment_obj.comment = "{}\n<<< {} >>>\n{}".format(comment_obj.comment, now, request.POST['comment_text'])
        comment_obj.save()

    return JsonResponse(dict(success=True))


@login_required
@csrf_exempt
def save_comment(request, comment_id):
    comment = LBComment.objects.filter(id__exact=comment_id).all()
    if len(comment):
        comment_obj = comment[0]
        if request.user.id == comment_obj.user.id:
            now = datetime.datetime.now().isoformat()
            #comment_obj.comment = "{}\n<<< {} >>>\n{}".format(comment_obj.comment, now, request.POST['comment_text'])
            comment_obj.comment = request.POST['comment_text']
            comment_obj.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def get_g_comments(request, place_id):
    try:
        place = LBPlace.objects.get(id__exact=place_id)
        comments = place.positive_comment.order_by("-createDate").all()
        comments = [p.to_detail() for p in comments]
    except Exception as e:
        comments = []
        print("{}".format(e))
    return JsonResponse(dict(comments=comments))


@login_required
def get_b_comments(request, place_id):
    try:
        place = LBPlace.objects.get(id__exact=place_id)
        comments = place.negative_comment.order_by("-createDate").all()
        comments = [p.to_detail() for p in comments]
    except Exception as e:
        comments = []
        print("{}".format(e))
    return JsonResponse(dict(comments=comments))
