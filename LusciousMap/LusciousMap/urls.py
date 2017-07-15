"""LusciousMap URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin, sitemaps
from django.contrib.sitemaps.views import sitemap
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.views.generic import TemplateView

from frontend.column.models import LMColumn
from frontend.map_basic.models import LMPlace
from frontend.map_map.models import LMMap


class LMMapSitemap(sitemaps.Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return LMMap.objects.filter(display__exact=True)

    def lastmod(self, obj):
        return obj.updateDate

    def location(self, item):
        return reverse('map_view', args=[item.id])


class LMPlaceSitemap(sitemaps.Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return LMPlace.objects.filter(display__exact=True)

    def lastmod(self, obj):
        return obj.updateDate

    def location(self, item):
        return reverse('place_view', args=[item.id])


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['index', 'column_index']

    def location(self, item):
        return reverse(item)


class ColumnSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return LMColumn.objects.filter(display__exact=True)

    def lastmod(self, obj):
        return obj.updateDate

    def location(self, item):
        return reverse('column_detail', args=[item.id])

sitemaps = {
    'column': ColumnSitemap,
    'map': LMMapSitemap,
    'place': LMPlaceSitemap,
    'static': StaticViewSitemap,
}

urlpatterns = [
    url(r'^google83bbd874881151b1.html$', TemplateView.as_view(template_name='google/google83bbd874881151b1.html')),
    url(r'^admin/', admin.site.urls),
    # url(r'', include('frontend.main.urls')),
    url(r'^accounts/', include('allauth.urls')),
    # api
    url(r'^api/', include('api.api.urls')),
    # sitemap
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap')
]

urlpatterns += i18n_patterns(
    url(_(r''), include('frontend.main.urls')),
    url(_(r''), include('frontend.map_basic.urls')),
    url(_(r''), include('frontend.map_map.urls')),
)
