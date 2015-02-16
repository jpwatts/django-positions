from django.db import models

import positions


class Item(models.Model):
    description = models.CharField(max_length=50)

    # I'm calling the PositionField "index" to make sure any internal code that
    # relies on a PositionField being called "position" will break.
    # https://github.com/jpwatts/django-positions/pull/12
    index = positions.PositionField()

    objects = positions.PositionManager('index')

    def __unicode__(self):
        return self.description
