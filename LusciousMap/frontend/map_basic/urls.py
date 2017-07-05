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

from frontend.map_basic import views

urlpatterns = [
    url(r'^place/detail/(?P<place_id>[\w\-]+)/$', views.place_detail, name="place_detail"),
    url(r'^place/search/$', views.search_place, name="search_place"),
    url(r'^tag/search/$', views.search_tag, name="search_tag"),
    url(r'^place/edit/new/$', views.new_place, name="edit_new_place"),
    # rating
    url(r'^place/good/(?P<place_id>[\w\-]+)/$', views.good_to_place, name="good_place"),
    url(r'^place/bad/(?P<place_id>[\w\-]+)/$', views.bad_to_place, name="bad_place"),
]
