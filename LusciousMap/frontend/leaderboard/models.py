import uuid
from datetime import timezone, timedelta

from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.urls import reverse

from frontend.map_basic.models import LMTag, LMPlace, LMPhoto


class LBComment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    createDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(auto_now=True)

    comment = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    iamlocal = models.BooleanField(default=False)

    def to_detail(self):
        fb_profile_pic_url = SocialAccount.objects.get(user_id__exact=self.user.id).extra_data['id']
        fb_profile_pic_url = "http://graph.facebook.com/{}/picture".format(fb_profile_pic_url)
        return dict(id=self.id,
                    save_url=reverse('leaderboard_save_comment', args=[self.id]),
                    comment_str=self.comment.replace("\n", "<br>"),
                    comment=self.comment,
                    update_date=self.updateDate,
                    update_date_str=self.pretty_date(self.updateDate),
                    create_date_str=self.pretty_date(self.createDate),
                    iamlocal=self.iamlocal,
                    username=self.user.username,
                    user=dict(username=self.user.username,
                              id=self.user.id,
                              fb_profile_pic_url=fb_profile_pic_url),
                    )

    def pretty_date(self, time=False):
        """
        Get a datetime object or a int() Epoch timestamp and return a
        pretty string like 'an hour ago', 'Yesterday', '3 months ago',
        'just now', etc
        """
        from datetime import datetime
        now = datetime.now(timezone.utc)
        if type(time) is int:
            diff = now - datetime.fromtimestamp(time)
        elif isinstance(time, datetime):
            diff = now - time
        elif not time:
            diff = now - now
        second_diff = diff.seconds
        day_diff = diff.days

        if day_diff < 0:
            return ''

        if day_diff == 0:
            if second_diff < 10:
                return "剛剛"
            if second_diff < 60:
                return str(second_diff) + " 秒前"
            if second_diff < 120:
                return "a minute ago"
            if second_diff < 3600:
                return "{:.0f}".format(second_diff / 60) + " 分鐘前"
            if second_diff < 7200:
                return "1個小時前"
            if second_diff < 86400:
                return "{:.0f}".format(second_diff / 3600) + " 小時前"
        if day_diff == 1:
            return "昨天"
        if day_diff < 7:
            return str(day_diff) + " 天前"
        if day_diff < 31:
            return "{:.0f}".format(day_diff / 7) + " 星期前"
        if day_diff < 365:
            return "{:.0f}".format(day_diff / 30) + " 月前"
        return "{:.0f}".format(day_diff / 365) + " 年前"


class LBPlace(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    createDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(auto_now=True)
    last_updateDate = models.DateTimeField(auto_now_add=True)

    rating_good_score = models.FloatField(default=0)
    rating_good_index = models.IntegerField(default=0)
    rating_good_last_index = models.IntegerField(default=0)

    rating_bad_score = models.FloatField(default=0)
    rating_bad_index = models.IntegerField(default=0)
    rating_bad_last_index = models.IntegerField(default=0)

    place = models.ForeignKey(LMPlace, null=True, blank=True, on_delete=models.DO_NOTHING)
    positive_comment = models.ManyToManyField(LBComment, blank=True, related_name='lbplace_g_lbcomment')
    negative_comment = models.ManyToManyField(LBComment, blank=True, related_name='lbplace_b_lbcomment')

    def __str__(self):
       return self.place.name

    def to_detail(self):
        return dict(id=self.id,
                    place=self.place.as_detail(),
                    rating_good_score=self.rating_good_score,
                    rating_good_index=self.rating_good_index,
                    rating_good_last_index=self.rating_good_last_index,
                    rating_bad_score=self.rating_good_score,
                    rating_bad_index=self.rating_bad_index,
                    rating_bad_last_index=self.rating_bad_last_index,

                    positive_comment=[p.to_detail() for p in self.positive_comment.all()],
                    negative_comment=[p.to_detail() for p in self.negative_comment.all()],

                    total_count=self.positive_comment.count()+self.negative_comment.count(),
                    positive_comment_count=self.positive_comment.count(),
                    negative_comment_count=self.negative_comment.count(),
                    positive_url=reverse('webplugin_leaderplace_positive', args=[self.id]),
                    negative_url=reverse('webplugin_leaderplace_negative', args=[self.id]),
                    save_g_comment_url=reverse('leaderboard_save_g_comment', args=[self.id]),
                    save_b_comment_url=reverse('leaderboard_save_b_comment', args=[self.id]),)


class LBTopic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    createDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(auto_now=True)

    title = models.CharField(max_length=255)
    display = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)

    tags = models.ManyToManyField(LMTag, blank=True, related_name='lbtopic_lm_tag')

    places = models.ManyToManyField(LBPlace, blank=True, related_name='lbtopic_lbplace')

    cover_photo = models.ForeignKey(LMPhoto, null=True, blank=True, on_delete=models.CASCADE,
                                  related_name='lbtopic_lm_photo')

    def to_detail(self):
        positive_comment_count = [a.positive_comment.count() for a in self.places.all()]
        positive_comment_count = sum(positive_comment_count)
        negative_comment_count = [a.negative_comment.count() for a in self.places.all()]
        negative_comment_count = sum(negative_comment_count)

        total_count = self.places.count()

        return dict(id=self.id,
                    title=self.title,
                    description=self.description,
                    total_count=total_count,
                    positive_comment_count=positive_comment_count,
                    negative_comment_count=negative_comment_count,
                    next_updatedate=self.updateDate + timedelta(hours=1))

    def __str__(self):
       return self.title


@receiver(models.signals.pre_save, sender=LBTopic)
def post_delete_lmplace_on_delete(sender, instance, **kwargs):
    try:
        old = LBTopic.objects.get(id__exact=instance.id)
        if instance.cover_photo != old.cover_photo:
            if old.cover_photo is not None:
                old.cover_photo.delete()
    except Exception as e:
        print("{}".format(e))
