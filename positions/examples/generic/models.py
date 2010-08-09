from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import models

from positions.fields import PositionField


class GenericThing(models.Model):
    name = models.CharField(max_length=80)
    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType)
    content_object = generic.GenericForeignKey()
    position = PositionField(collection=('object_id', 'content_type'))

    def __unicode__(self):
        return self.name
