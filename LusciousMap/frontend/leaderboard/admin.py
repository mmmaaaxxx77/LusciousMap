from django.contrib import admin
from django.contrib.admin import DateFieldListFilter
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms import ModelMultipleChoiceField, ModelForm

from frontend.leaderboard.models import LBComment, LBPlace, LBTopic
from frontend.map_basic.models import LMPlace


class LBPlaceAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'id', 'rating_good_index', 'rating_bad_index')
    search_fields = ('rating_good_index', 'rating_bad_index')
    list_filter = (('createDate', DateFieldListFilter), ('updateDate', DateFieldListFilter))

    def get_name(self, obj):
        return obj.place.name


class LBTopicAdminForm(ModelForm):
    places = ModelMultipleChoiceField(queryset=LBPlace.objects.all(),
                                    widget=FilteredSelectMultiple("name", is_stacked=False))
    class Meta:
        model = LBTopic
        fields = '__all__'


class LBTopicAdmin(admin.ModelAdmin):
    form = LBTopicAdminForm

    list_display = ('title', )
    search_fields = ('id', 'title', 'description')
    list_filter = ('display', ('createDate', DateFieldListFilter), ('updateDate', DateFieldListFilter))


class LBCommentAdmin(admin.ModelAdmin):
    list_display = ('comment', 'iamlocal')
    search_fields = ('id', 'comment')
    list_filter = (('createDate', DateFieldListFilter), ('updateDate', DateFieldListFilter))

admin.site.register(LBComment, LBCommentAdmin)
admin.site.register(LBPlace, LBPlaceAdmin)
admin.site.register(LBTopic, LBTopicAdmin)
