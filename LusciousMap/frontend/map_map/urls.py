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

from frontend.map_map.views import views
from frontend.map_map.views import edit

urlpatterns = [
    url(r'^map/place/search/$', views.search_place, name="search_map_place"),
    url(r'^map/place/list/$', views.search_place_list, name="search_map_place_list"),
    url(r'^map/place/list/init$', views.init_recommend_list, name="init_recommend_list"),
    # rating
    url(r'^map/good/(?P<place_id>[\w\-]+)/$', views.good_to_map, name="good_map"),
    url(r'^map/bad/(?P<place_id>[\w\-]+)/$', views.bad_to_map, name="bad_map"),
    # edit
    url(r'^map/detail/(?P<map_id>[\w\-]+)/$', edit.detail_map, name="detail_map"),
    url(r'^mapplace/detail/(?P<place_id>[\w\-]+)/$', edit.detail_mapplace, name="detail_mapplace"),
    url(r'^map/save/$', edit.edit_map, name="save_map"),
    url(r'^mapplace/list/$', edit.list_mapplace, name="list_mapplace"),
    url(r'^map/list/$', edit.list_map, name="list_map"),
    url(r'^follow/list/$', edit.list_follows, name="list_follows"),
    url(r'^map/mark/save$', edit.save_map_mark, name="save_map_mark"),
]
