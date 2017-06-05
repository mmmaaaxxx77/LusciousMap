from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.dispatch import receiver
from allauth.account.signals import user_signed_up


@login_required
def index(request):
    """
    try:
        social_user = SocialAccount.objects.get(user__exact=request.user)
        print(social_user.uid)
        #user = request.user
        #user.username = user.first_name + user.last_name
        #user.save()
    except:
        pass
    print(request.user.username)
    """

    return render(request, "index/index.html", {})


def new_place(request):
    return render(request, "place/new_place.html", {})


def map_view(request):
    return render(request, "place/map_view.html", {})


def map_edit(request):
    return render(request, "place/map_edit.html", {})
