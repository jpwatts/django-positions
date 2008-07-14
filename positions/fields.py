import logging

from django.db import connection, models
from django.db.models.signals import post_delete, post_save
from django.dispatch import dispatcher


qn = connection.ops.quote_name


class PositionField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, unique_for_field=None,
                 *args, **kwargs):
        kwargs.setdefault('blank', True)

        # unique constraints break the ability to execute a single query to
        # increment or decrement a set of positions; they also require the use
        # of temporary placeholder positions which result in undesirable
        # additional queries
        unique = kwargs.get('unique', False)
        if unique:
            raise TypeError('%s cannot have a unique constraint' % self.name)

        # TODO: raise exception if position field appears in unique_together

        super(PositionField, self).__init__(verbose_name, name, *args, **kwargs)
        self.unique_for_field = unique_for_field

    def contribute_to_class(self, cls, name):
        super(PositionField, self).contribute_to_class(cls, name)

        # use this object as the descriptor for field access
        setattr(cls, self.name, self)

        # adjust related positions in response to a delete or save
        dispatcher.connect(self._on_delete, sender=cls, signal=post_delete)
        dispatcher.connect(self._on_save, sender=cls, signal=post_save)

    def get_internal_type(self):
        # all values will be positive after pre_save
        return 'PositiveIntegerField'

    def pre_save(self, model_instance, add):
        current, updated = self._get_instance_cache(model_instance)

        logging.debug('pre_save: current=%s; updated=%s' % (current, updated))

        # existing instance, position not modified; no cleanup required
        if current is not None and updated is None:
            self._reset_instance_cache(model_instance, current)
            return current

        count = self._get_instance_peers(model_instance).count()
        if current is None:
            max_position = count
        else:
            max_position = count - 1
        min_position = 0

        logging.debug(
            'pre_save: max_position=%s; min_position=%s' % (max_position,
                                                            min_position)
        )

        # new instance; appended; no cleanup required
        if current is None and (updated == -1 or updated >= max_position):
            self._reset_instance_cache(model_instance, max_position)
            return max_position

        if max_position >= updated >= min_position:
            # positive position; valid index
            position = updated
        elif updated > max_position:
            # positive position; invalid index
            position = max_position
        elif abs(updated) <= (max_position + 1):
            # negative position; valid index
            position = max_position + 1 + updated
        else:
            # negative position; invalid index
            position = min_position

        logging.debug('pre_save: position=%s' % position)

        # instance inserted; cleanup required on post_save
        self._set_instance_cache(model_instance, position)
        return position

    def __get__(self, instance, owner):
        if instance is None:
            raise AttributeError('%s must be accessed via instance' % self.name)
        current, updated = self._get_instance_cache(instance)
        if updated is None:
            return current
        return updated

    def __set__(self, instance, value):
        if instance is None:
            raise AttributeError('%s must be accessed via instance' % self.name)
        self._set_instance_cache(instance, value)

    def _get_instance_cache(self, instance):
        try:
            current, updated = getattr(instance, self.get_cache_name())
        except (AttributeError, TypeError):
            current, updated = None, None
        return current, updated

    def _reset_instance_cache(self, instance, value):
        try:
            delattr(instance, self.get_cache_name())
        except AttributeError:
            pass
        setattr(instance, self.get_cache_name(), (value, None))

    def _set_instance_cache(self, instance, value):
        # TODO: Find a more robust way to determine if instance exists in
        # the db; this is necessary because the position field won't be
        # initialized to None when models.Manager.create is called with an
        # explicit position.

        # FIXME: This breaks pre-newforms-admin when setting a position gt the
        # maximum possible position -- something about how models are
        # instantiated keeps this method from doing the right thing.
        # Fortunately it works on newforms-admin, so it will be moot soon.

        has_pk = bool(getattr(instance, instance._meta.pk.attname))

        # default to None for existing instances; -1 for new instances
        updated = None if has_pk else -1

        try:
            current = getattr(instance, self.get_cache_name())[0]
        except (AttributeError, TypeError):
            if has_pk:
                current = value
            else:
                current = None
                if value is not None:
                    updated = value
        else:
            if value is None:
                updated = -1
            elif value != current:
                updated = value

        setattr(instance, self.get_cache_name(), (current, updated))

    def _get_instance_peers(self, instance):
        filters = {}
        if self.unique_for_field:
            filters[self.unique_for_field] = getattr(instance,
                                                     self.unique_for_field)
        return instance.__class__._default_manager.filter(**filters)

# TODO: refactor _on_delete and _on_save to remove the blatant copy-paste job

    def _on_delete(self, sender, instance):
        current, updated = self._get_instance_cache(instance)
        
        logging.debug('_on_delete: current=%s; updated=%s' % (current, updated))

        params = {
            'position_field': qn(self.column),
            'table': qn(instance._meta.db_table),
        }

        query = """
        UPDATE %(table)s
        SET %(position_field)s = (%(position_field)s - 1)"""

        wheres = []

        if self.unique_for_field:
            unique_for_field = instance._meta.get_field(self.unique_for_field)
            params.update({
                'unique_for_field': qn(unique_for_field.column),
                'unique_for_field_pk': getattr(instance,
                                               unique_for_field.attname)
            })
            wheres.append('%(unique_for_field)s = %(unique_for_field_pk)s')

        # decrement positions gt current
        gt_or_lt_position = '%%(position_field)s %(gt_or_lt)s %(position)s'
        wheres.append(gt_or_lt_position % {
            'gt_or_lt': '>',
            'position': current,
        })

        query += ' WHERE %s' % ' AND '.join(wheres)
        cursor = connection.cursor()
        cursor.execute(query % params)
        self._reset_instance_cache(instance, updated)

    def _on_save(self, sender, instance):
        current, updated = self._get_instance_cache(instance)

        logging.debug('_on_save: current=%s; updated=%s' % (current, updated))

        # no cleanup required
        if updated is None:
            return None

        params = {
            'pk_field': qn(instance._meta.pk.column),
            'pk': getattr(instance, instance._meta.pk.attname),
            'position_field': qn(self.column),
            'table': qn(instance._meta.db_table),
        }

        # TODO: correctly handle auto_now date(time) fields

        query = """
        UPDATE %(table)s
        SET %(position_field)s = (%(position_field)s %(plus_or_minus)s 1)"""

        wheres = []

        if self.unique_for_field:
            unique_for_field = instance._meta.get_field(self.unique_for_field)
            params.update({
                'unique_for_field': qn(unique_for_field.column),
                'unique_for_field_pk': getattr(instance,
                                               unique_for_field.attname)
            })
            wheres.append('%(unique_for_field)s = %(unique_for_field_pk)s')

        gt_or_lt_position = '%%(position_field)s %(gt_or_lt)s %(position)s'

        if current is None:
            # increment positions gte updated; excluding instance
            params['plus_or_minus'] = '+'
            wheres.append(gt_or_lt_position % {
                'gt_or_lt': '>=',
                'position': updated,
            })
        elif updated > current:
            # decrement positions gt current and lte updated; excluding instance
            params['plus_or_minus'] = '-'
            wheres.append(gt_or_lt_position % {
                'gt_or_lt': '>',
                'position': current,
            })
            wheres.append(gt_or_lt_position % {
                'gt_or_lt': '<=',
                'position': updated,
            })
        else:
            # increment positions lt current and gte updated; excluding instance
            params['plus_or_minus'] = '+'
            wheres.append(gt_or_lt_position % {
                'gt_or_lt': '>=',
                'position': updated,
            })
            wheres.append(gt_or_lt_position % {
                'gt_or_lt': '<',
                'position': current,
            })

        wheres.append('%(pk_field)s != %(pk)s')

        query += ' WHERE %s' % ' AND '.join(wheres)
        cursor = connection.cursor()
        cursor.execute(query % params)
        self._reset_instance_cache(instance, updated)
