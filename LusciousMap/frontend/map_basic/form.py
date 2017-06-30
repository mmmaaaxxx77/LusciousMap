from django import forms


class ImageUploadForm(forms.Form):
    """Image upload form."""
    picture = forms.ImageField()
    name = forms.CharField()


class MapUploadForm(forms.Form):
    """Image upload form."""
    map_picture = forms.ImageField()
