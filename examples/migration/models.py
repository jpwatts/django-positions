from django.db import models

from positions.fields import PositionField


class MigrationTest(models.Model):
    name = models.CharField(max_length=80)
    age = models.IntegerField(null=True, blank=True)
    favorite_color = models.CharField(max_length=255, null=True, blank=True)
    position = PositionField(collection=('name', 'age'))

    def __unicode__(self):
        return self.name