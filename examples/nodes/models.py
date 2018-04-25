from django.db import models
from positions.fields import PositionField

class Node(models.Model):
    parent = models.ForeignKey('self', related_name='children', blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    position = PositionField(collection='parent')

    def __unicode__(self):
       return self.name
