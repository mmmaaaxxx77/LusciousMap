import random
import datetime
from frontend.google_service.models import ServiceKey


def service_key_getter(type):
    key = find_enable_key(type)
    return key.key


def find_enable_key(type):
    keys = ServiceKey.objects.filter(type__exact=type).all()
    key = random.choice(list(keys))

    now_month = datetime.date.today().month
    last_month = key.last_month_key_get.month

    if now_month != last_month:
        key.disable = False
        key.count = 0
    elif now_month == last_month and key.count >= 25000:
        key.disable = True
        key.save()
        key = find_enable_key(type)

    key.count = key.count+1

    key.save()

    return key