from django.db import models

from positions import PositionField


class Album(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class Photo(models.Model):
    album = models.ForeignKey(Album, related_name='photos', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    position = PositionField(collection='album', default=0)

    def __unicode__(self):
        return self.name
