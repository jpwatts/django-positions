from django.contrib.contenttypes.models import ContentType
try:
    from django.contrib.contenttypes.generic import GenericForeignKey
except ImportError:
    from django.contrib.contenttypes.fields import GenericForeignKey

from django.db import models

from positions.fields import PositionField


class GenericThing(models.Model):
    name = models.CharField(max_length=80)
    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_object = GenericForeignKey()
    position = PositionField(collection=('object_id', 'content_type'))

    def __unicode__(self):
        return self.name
