import random
import datetime
from frontend.google_service.models import ServiceKey


def service_key_getter(type):
    key = find_enable_key(type)
    return key.key


def find_enable_key(type):
    keys = ServiceKey.objects.filter(type__exact=type).all()
    key = random.choice(list(keys))

    now_day = datetime.date.today().day
    last_day = key.last_month_key_get.day

    if type == 0:
        limit = 9000
    else:
        limit = 1999

    if now_day != last_day:
        key.last_month_key_get = datetime.date.today()
        key.disable = False
        key.count = 0
    elif now_day == last_day and key.count >= limit:
        key.disable = True
        key.save()
        key = find_enable_key(type)

    key.count = key.count+1

    key.save()

    return key