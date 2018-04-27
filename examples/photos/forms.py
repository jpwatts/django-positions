from django import forms

from examples.photos.models import Photo


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo 
        fields = ['name',]
