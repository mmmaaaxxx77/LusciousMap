"""LusciousMap URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.views.generic import TemplateView

from frontend.main.views import views, column, leaderboard
from frontend.main.views import webplugin

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^google83bbd874881151b1.html$', TemplateView.as_view(template_name='google/google83bbd874881151b1.html')),
    url(r'^place/new/$', views.new_place, name="new_place"),
    url(r'^place/view/(?P<place_id>[\w\-]+)/$', views.place_view, name="place_view"),
    url(r'^map/view/(?P<map_id>[\w\-]+)/$', views.map_view, name="map_view"),
    url(r'^map/edit/$', views.map_edit, name="map_edit"),
    url(r'^photo/(?P<image_id>[\w\-]+)/$', views.get_photo, name="get_photo"),
    url(r'^photothumbnail/(?P<image_id>[\w\-]+)/$', views.get_photo_thumbnail, name="get_photothumbnail"),
    url(r'^index/detail/$', views.get_index_detail, name="get_index_detail"),
    # webplugin
    url(r'^webplugin/map/(?P<map_id>[\w\-]+)/$', webplugin.map, name="webplugin_map"),
    url(r'^webplugin/place/(?P<place_id>[\w\-]+)/$', webplugin.place, name="webplugin_place"),
    # column
    url(r'^column/$', column.index, name="column_index"),
    url(r'^column/search/$', column.search_column, name="column_search"),
    url(r'^column/detail/(?P<column_id>[\w\-]+)/$', column.detail, name="column_detail"),
    # leaderboard
    url(r'^leaderboard/$', leaderboard.index, name="leaderboard_index"),
    url(r'^leaderboard/detail/(?P<topic_id>[\w\-]+)/$', leaderboard.detail, name="leaderboard_detail"),
    url(r'^leaderboard/topic/(?P<topic_id>[\w\-]+)/$', leaderboard.get_topic, name="leaderboard_get_topic"),
    url(r'^leaderboard/placeslist/positive/(?P<topic_id>[\w\-]+)/$', leaderboard.get_g_places,
        name="leaderboard_get_positive_places"),
    url(r'^leaderboard/placeslist/negative/(?P<topic_id>[\w\-]+)/$', leaderboard.get_b_places,
        name="leaderboard_get_negative_places"),
    url(r'^leaderboard/search/(?P<topic_id>[\w\-]+)/$', leaderboard.search_places, name="leaderboard_search"),
    url(r'^leaderboard/save/comment/positive/(?P<place_id>[\w\-]+)/$', leaderboard.save_g_comment,
        name="leaderboard_save_g_comment"),
    url(r'^leaderboard/save/comment/negative/(?P<place_id>[\w\-]+)/$', leaderboard.save_b_comment,
        name="leaderboard_save_b_comment"),
    url(r'^leaderboard/list/comment/negative/(?P<place_id>[\w\-]+)/$', leaderboard.get_b_comments,
        name="leaderboard_list_b_comment"),
    url(r'^leaderboard/list/comment/positive/(?P<place_id>[\w\-]+)/$', leaderboard.get_g_comments,
        name="leaderboard_list_g_comment"),
    url(r'^leaderboard/save/comment/all/(?P<comment_id>[\w\-]+)/$', leaderboard.save_comment,
        name="leaderboard_save_comment"),
]
