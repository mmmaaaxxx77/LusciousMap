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

from frontend.main.views import views
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
]
