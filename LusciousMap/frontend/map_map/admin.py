from django.contrib import admin
from django.contrib.admin import DateFieldListFilter

from frontend.map_map.models import LMMapPlace, LMMap, LMUserDetail


class LMMapPlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'display', 'user')
    search_fields = ('name', 'user__username', 'place__google_place_id')
    list_filter = ('place__place_type', 'display', 'place__country', ('createDate', DateFieldListFilter), 'user')


class LMMapAdmin(admin.ModelAdmin):
    list_display = ('name', 'display', 'user')
    search_fields = ('name', 'user__username')
    list_filter = ('display', ('createDate', DateFieldListFilter), 'user')


admin.site.register(LMMapPlace, LMMapPlaceAdmin)
admin.site.register(LMMap, LMMapAdmin)
admin.site.register(LMUserDetail)
