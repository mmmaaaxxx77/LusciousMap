import uuid

from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.urls import reverse

from frontend.map_basic.models import LMTag, LMPhoto


class LMColumn(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    createDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(auto_now=True)

    title = models.CharField(max_length=255)
    display = models.BooleanField(default=True)
    content = models.TextField(blank=True, null=True)
    short_description = models.TextField(blank=True, null=True)

    tags = models.ManyToManyField(LMTag, blank=True, related_name='lm_column_lm_tag')

    hide_tags = models.ManyToManyField(LMTag, blank=True, related_name='lm_column_hide_lm_tag')

    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.DO_NOTHING)

    cover_photo = models.ForeignKey(LMPhoto, null=True, blank=True, on_delete=models.CASCADE,
                                  related_name='lm_column_lm_photo')

    def as_json(self):
        return dict(
            id=self.id,
            title=self.title,
            display=self.display,
            short_description=self.short_description,
            tags=[a.as_json() for a in self.tags.all()],
            cover_photo=self.cover_photo.as_json(),
            url=reverse('column_detail', args=[self.id]),
            update_str=self.updateDate.strftime("%Y %m %d"),
        )

    def as_detail(self):
        return dict(
            id=self.id,
            title=self.title,
            display=self.display,
            content=self.content,
            short_description=self.short_description,
            tags=[a.as_json() for a in self.tags.all()],
            cover_photo=self.cover_photo.as_json()
        )

@receiver(models.signals.pre_save, sender=LMColumn)
def post_delete_lmplace_on_delete(sender, instance, **kwargs):
    try:
        old = LMColumn.objects.get(id__exact=instance.id)
        if instance.cover_photo != old.cover_photo:
            if old.cover_photo is not None:
                old.cover_photo.delete()
    except Exception as e:
        print("{}".format(e))

