from django.db import models

from positions.fields import PositionField


class List(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class Item(models.Model):
    list = models.ForeignKey('list', related_name='items', db_index=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    position = PositionField(collection='list')
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name
