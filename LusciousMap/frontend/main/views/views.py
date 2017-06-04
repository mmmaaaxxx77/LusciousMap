from django.http import HttpResponse
from django.shortcuts import render
from django.utils.translation import gettext as _


def index(request):
    return render(request, "index/index.html", {})


def new_place(request):
    return render(request, "place/new_place.html", {})


def map_view(request):
    return render(request, "place/map_view.html", {})


def map_edit(request):
    return render(request, "place/map_edit.html", {})
