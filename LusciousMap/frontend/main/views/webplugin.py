from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse

from frontend.leaderboard.models import LBPlace
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


@login_required
def leaderboard_negative_place(request, place_id):
    place = LBPlace.objects.get(id__exact=place_id)
    return render(request, "webplugin/leaderboard_comment.html",
                  dict(
                      url=reverse('webplugin_leaderplace_negative', args=[place.id]),
                      c_id="{}{}".format(place.id, "negative"),
                      comment_url=place.to_detail()['save_b_comment_url'],
                      comments_list_url=reverse('leaderboard_list_b_comment', args=[place.id]),
                      panel_css="panel-danger",
                  ))


@login_required
def leaderboard_positive_place(request, place_id):
    place = LBPlace.objects.get(id__exact=place_id)
    return render(request, "webplugin/leaderboard_comment.html",
                  dict(
                      url=reverse('webplugin_leaderplace_positive', args=[place.id]),
                      c_id="{}{}".format(place.id, "positive"),
                      comment_url=place.to_detail()['save_g_comment_url'],
                      comments_list_url=reverse('leaderboard_list_g_comment', args=[place.id]),
                      panel_css="panel-info",
                  ))
