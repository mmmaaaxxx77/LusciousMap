from django.contrib import admin
from django.contrib.admin import ModelAdmin, DateFieldListFilter
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms import ModelForm, Textarea, ModelMultipleChoiceField

from frontend.column.models import LMColumn
from frontend.map_basic.models import LMTag


class LMColumnAdminForm(ModelForm):
    tags = ModelMultipleChoiceField(queryset=LMTag.objects.all(),
                                    widget=FilteredSelectMultiple("name", is_stacked=False))
    hide_tags = ModelMultipleChoiceField(queryset=LMTag.objects.all(),
                                    widget=FilteredSelectMultiple("name", is_stacked=False))
    class Meta:
        model = LMColumn
        widgets = {
            'content': Textarea(attrs={'class': 'ckeditor'}),
        }
        fields = '__all__'


class LMColumnAdmin(ModelAdmin):
    form = LMColumnAdminForm
    """
    formfield_overrides = {
        TextField: {'widget': Textarea(attrs={'class': 'ckeditor'})},
    }
    """
    list_display = ('id', 'title',)
    search_fields = ('id', 'title',)
    list_filter = (('createDate', DateFieldListFilter),)

    class Media:
        js = ('/static/frontend//plugins/ckeditor/ckeditor.js',)
        css = {
            'all': ('/static/frontend/plugins/ckeditor/djangoAdminCustomizer.css',)
        }


admin.site.register(LMColumn, LMColumnAdmin)
