import uuid

import datetime
from django.db import models


class ServiceKey(models.Model):

    TYPE = (
        (0, 'MAP'),
        (1, 'STATICMAP'),
        (2, 'MAPDETAIL'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    key = models.CharField(max_length=225)
    type = models.IntegerField(choices=TYPE, default=0)
    count = models.IntegerField(default=0)
    last_month_key_get = models.DateTimeField(default=datetime.datetime.now, blank=True)
    disable = models.BooleanField(default=False)

    def __str__(self):
       return "{} {}: {}".format(self.TYPE[self.type][1], self.disable, self.key)

