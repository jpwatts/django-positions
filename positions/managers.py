from django.db.models import Manager
from django.db.models.query import QuerySet
from django.db.models.signals import post_save

from positions.fields import PositionField


class PositionQuerySet(QuerySet):
    def __init__(self, model=None, query=None, using=None, position_field_name='position'):
        super(PositionQuerySet, self).__init__(model, query, using)
        self.position_field_name = position_field_name

    def reposition(self, save=True):
        position_field = self.model._meta.get_field_by_name(self.position_field_name)[0]
        post_save.disconnect(position_field.update_on_save, sender=self.model)
        position = 0
        for obj in self.iterator():
            setattr(obj,self.position_field_name,position)
            if save:
                obj.save()
            position += 1
        post_save.connect(position_field.update_on_save, sender=self.model)
        return self


class PositionManager(Manager):
    def __init__(self, position_field_name='position'):
        super(PositionManager, self).__init__()
        self.position_field_name = position_field_name

    def get_query_set(self):
        return PositionQuerySet(self.model, position_field_name=self.position_field_name)

    def reposition(self):
        return self.get_query_set().reposition()
