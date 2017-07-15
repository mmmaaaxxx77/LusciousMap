from django.contrib import admin

# Register your models here.
from django.contrib.admin import DateFieldListFilter

from frontend.map_basic.models import LMCountry, LMCity, LMAttraction, LMPhoto, LMRating, LMPlaceType, LMPlace, LMTag



def make_all_display(modeladmin, request, queryset):
    queryset.update(display=True)
make_all_display.short_description = "Mark selected place display"


class LMPlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'google_place_id', 'display', 'place_type', 'country')
    search_fields = ('name', 'user__username', 'google_place_id')
    list_filter = ('place_type', 'display', 'country', ('createDate', DateFieldListFilter), 'user')
    actions = [make_all_display]


class LMTagAdmin(admin.ModelAdmin):
    search_fields = ('name', 'createUser__username')
    list_filter = ('createUser',)


class LMCountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'long_name')


class LMPlaceTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


admin.site.register(LMTag, LMTagAdmin)
admin.site.register(LMCountry, LMCountryAdmin)
admin.site.register(LMCity)
admin.site.register(LMAttraction)
admin.site.register(LMPhoto)
admin.site.register(LMRating)
admin.site.register(LMPlaceType, LMPlaceTypeAdmin)
admin.site.register(LMPlace, LMPlaceAdmin)
