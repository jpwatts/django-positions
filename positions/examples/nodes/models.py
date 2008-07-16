from django.db import models, transaction

from positions.fields import PositionField


class Node(models.Model):
    parent = models.ForeignKey('self', related_name='children', blank=True,
                               null=True)
    name = models.CharField(max_length=50)
    position = PositionField(unique_for_field='parent')

    def __unicode__(self):
       return self.name

    save = transaction.commit_on_success(models.Model.save)
