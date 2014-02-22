from django import forms

from positions.examples.photos.models import Photo


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo 
        fields = ['name',]
