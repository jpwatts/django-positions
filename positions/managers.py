from django.db.models import Manager
from django.db.models.query import QuerySet
from django.db.models.signals import post_save

from positions.fields import PositionField

import logging
logger = logging.getLogger(__name__)

class PositionQuerySet(QuerySet):
    def __init__(self, model=None, query=None, using=None, position_field_name='position', hints=None):
        super(PositionQuerySet, self).__init__(model, query, using)
        self.position_field_name = position_field_name

    def _clone(self, *args, **kwargs):
        queryset = super(PositionQuerySet, self)._clone(*args, **kwargs)
        queryset.position_field_name = self.position_field_name
        return queryset

    def reposition(self, save=True):
        try:
            position_field = self.model._meta.get_field_by_name(self.position_field_name)[0]
        except AttributeError:
            # Handle Django 1.10+ which removes get_field_by_name
            position_field = self.model._meta.get_field(self.position_field_name)
        post_save.disconnect(position_field.update_on_save, sender=self.model)
        position = 0
        for obj in self.iterator():
            setattr(obj, self.position_field_name, position)
            if save:
                obj.save()
            position += 1
        post_save.connect(position_field.update_on_save, sender=self.model)
        return self


class PositionManager(Manager):
    def __init__(self, position_field_name='position'):
        super(PositionManager, self).__init__()
        self.position_field_name = position_field_name

    def get_queryset(self):
        return PositionQuerySet(self.model, position_field_name=self.position_field_name)

    def get_query_set(self):
        return self.get_queryset(self.model, position_field_name=self.position_field_name)

    def reposition(self):
        return self.get_queryset().reposition()
