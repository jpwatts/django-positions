import datetime
import warnings

from django.db import models
from django.db.models.signals import post_delete, post_save


class PositionField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, default=-1, collection=None, unique_for_field=None, unique_for_fields=None, *args, **kwargs):
        if 'unique' in kwargs:
            raise TypeError("%s can't have a unique constraint." % self.__class__.__name__)
        super(PositionField, self).__init__(verbose_name, name, default=default, *args, **kwargs)

        # Backwards-compatibility mess begins here.
        if collection is not None and unique_for_field is not None:
            raise TypeError("'collection' and 'unique_for_field' are incompatible arguments.")

        if collection is not None and unique_for_fields is not None:
            raise TypeError("'collection' and 'unique_for_fields' are incompatible arguments.")

        if unique_for_field is not None:
            warnings.warn("The 'unique_for_field' argument is deprecated.  Please use 'collection' instead.", DeprecationWarning)
            if unique_for_fields is not None:
                raise TypeError("'unique_for_field' and 'unique_for_fields' are incompatible arguments.")
            collection = unique_for_field

        if unique_for_fields is not None:
            warnings.warn("The 'unique_for_fields' argument is deprecated.  Please use 'collection' instead.", DeprecationWarning)
            collection = unique_for_fields
        # Backwards-compatibility mess ends here.

        if isinstance(collection, basestring):
            collection = (collection,)
        self.collection = collection

    def contribute_to_class(self, cls, name):
        super(PositionField, self).contribute_to_class(cls, name)
        for constraint in cls._meta.unique_together:
            if self.name in constraint:
                raise TypeError("%s can't be part of a unique constraint." % self.__class__.__name__)
        self.auto_now_fields = []
        for field in cls._meta.fields:
            if getattr(field, 'auto_now', False):
                self.auto_now_fields.append(field)
        setattr(cls, self.name, self)
        post_delete.connect(self.update_on_delete, sender=cls)
        post_save.connect(self.update_on_save, sender=cls)

    def get_internal_type(self):
        # pre_save always returns a value >= 0
        return 'PositiveIntegerField'

    def pre_save(self, model_instance, add):
        #NOTE: check if the node has been moved to another collection; if it has, delete it from the old collection.
        previous_instance = None
        collection_changed = False
        if add == False and self.collection:
            previous_instance = type(model_instance)._default_manager.get(pk=model_instance.pk)
            for field_name in self.collection:
                field = model_instance._meta.get_field(field_name)
                current_field_value = getattr(model_instance, field.attname)
                previous_field_value = getattr(previous_instance, field.attname)
                if previous_field_value != current_field_value:
                    collection_changed = True
                    break
        if collection_changed == False:
            previous_instance = None

        setattr(model_instance, 'collection_changed', collection_changed)
        if collection_changed:
            self.remove_from_collection(previous_instance)

        cache_name = self.get_cache_name()
        current, updated = getattr(model_instance, cache_name)

        if collection_changed:
            current = None

        if add:
            if updated is None:
                updated = current
            current = None

        # existing instance, position not modified; no cleanup required
        if current is not None and updated is None:
            return current

        collection_count = self.get_collection(model_instance).count()
        if current is None:
            max_position = collection_count
        else:
            max_position = collection_count - 1
        min_position = 0

        # new instance; appended; no cleanup required on post_save
        if add and (updated == -1 or updated >= max_position):
            setattr(model_instance, cache_name, (max_position, None))
            return max_position

        if max_position >= updated >= min_position:
            # positive position; valid index
            position = updated
        elif updated > max_position:
            # positive position; invalid index
            position = max_position
        elif abs(updated) <= (max_position + 1):
            # negative position; valid index

            # Add 1 to max_position to make this behave like a negative list index.
            # -1 means the last position, not the last position minus 1

            position = max_position + 1 + updated
        else:
            # negative position; invalid index
            position = min_position

        # instance inserted; cleanup required on post_save
        setattr(model_instance, cache_name, (current, position))
        return position

    def __get__(self, instance, owner):
        if instance is None:
            raise AttributeError("%s must be accessed via instance." % self.name)
        current, updated = getattr(instance, self.get_cache_name())
        return current if updated is None else updated

    def __set__(self, instance, value):
        if instance is None:
            raise AttributeError("%s must be accessed via instance." % self.name)
        if value is None:
            value = self.default
        cache_name = self.get_cache_name()
        try:
            current, updated = getattr(instance, cache_name)
        except AttributeError:
            current, updated = value, None
        else:
            updated = value
        setattr(instance, cache_name, (current, updated))

    def get_collection(self, instance):
        filters = {}
        if self.collection:
            for field_name in self.collection:
                field = instance._meta.get_field(field_name)
                field_value = getattr(instance, field.attname)
                if field.null and field_value is None:
                    filters['%s__isnull' % field.name] = True
                else:
                    filters[field.name] = field_value
        return type(instance)._default_manager.filter(**filters)

    def remove_from_collection(self, instance):
        """
        Removes a positioned item from the collection.
        """
        queryset = self.get_collection(instance)
        current = getattr(instance, self.get_cache_name())[0]
        updates = {self.name: models.F(self.name) - 1}
        if self.auto_now_fields:
            now = datetime.datetime.now()
            for field in self.auto_now_fields:
                updates[field.name] = now
        queryset.filter(**{'%s__gt' % self.name: current}).update(**updates)

    def update_on_delete(self, sender, instance, **kwargs):
        self.remove_from_collection(instance)

    def update_on_save(self, sender, instance, created, **kwargs):
        collection_changed = getattr(instance, 'collection_changed', False)

        current, updated = getattr(instance, self.get_cache_name())

        if updated is None and collection_changed == False:
            return None

        queryset = self.get_collection(instance).exclude(pk=instance.pk)

        updates = {}
        if self.auto_now_fields:
            now = datetime.datetime.now()
            for field in self.auto_now_fields:
                updates[field.name] = now

        if created or collection_changed:
            # increment positions gte updated or node moved from another collection
            queryset = queryset.filter(**{'%s__gte' % self.name: updated})
            updates[self.name] = models.F(self.name) + 1
        elif updated > current:
            # decrement positions gt current and lte updated
            queryset = queryset.filter(**{'%s__gt' % self.name: current, '%s__lte' % self.name: updated})
            updates[self.name] = models.F(self.name) - 1
        else:
            # increment positions lt current and gte updated
            queryset = queryset.filter(**{'%s__lt' % self.name: current, '%s__gte' % self.name: updated})
            updates[self.name] = models.F(self.name) + 1

        queryset.update(**updates)
        setattr(instance, self.get_cache_name(), (updated, None))

    def south_field_triple(self):
        from south.modelsinspector import introspector
        field_class = "django.db.models.fields.IntegerField"
        args, kwargs = introspector(self)
        return (field_class, args, kwargs)
