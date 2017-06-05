from django.contrib import admin

# Register your models here.
from frontend.map_basic.models import LMCountry, LMCity, LMAttraction, LMPhoto, LMRating, LMPlaceType, LMPlace

admin.site.register(LMCountry)
admin.site.register(LMCity)
admin.site.register(LMAttraction)
admin.site.register(LMPhoto)
admin.site.register(LMRating)
admin.site.register(LMPlaceType)
admin.site.register(LMPlace)
