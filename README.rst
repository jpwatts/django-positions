================
Django Positions
================

`Django Positions needs a new maintainer.`_ `I`_ wrote most of this code years
ago and haven't used it in a project for almost as long. I've tried to keep up
with bug reports and pull requests, but I've been doing an increasingly poor job
as Django has evolved and the test suite has begun to show its age. If you find
value in this project and are interested in taking it over, please get in touch
and I'll work with you to transfer control of the repository and `PyPI listing`_.

I'm sorry for not being a good maintainer of late and appreciate the interest,
and especially the contributions, this project has received. Thank you.

----

This module provides ``PositionField``, a model field for `Django`_ that allows
instances of a model to be sorted by a user-specified position.  Conceptually,
the field works like a list index: when the position of one item is changed, the
positions of other items in the collection are updated in response.


Usage
-----

Add a ``PositionField`` to your model; that's just about it.

If you want to work with all instances of the model as a single collection,
there's nothing else required.  To create collections based on one or more
fields on the model, specify the field names using the ``collection`` argument.

The apps in ``positions.examples`` demonstrate the ``PositionField`` API.


Indices
~~~~~~~

In general, the value assigned to a ``PositionField`` will be handled like a
list index, to include negative values.  Setting the position to ``-2`` will
cause the item to be moved to the second position from the end of collection --
unless, of course, the collection has fewer than two elements.

Behavior varies from standard list indices when values greater than or less than
the maximum or minimum positions are used.  In those cases, the value is handled
as being the same as the maximum or minimum position, respectively.  ``None`` is
also a special case that will cause an item to be moved to the last position in
its collection.

Bulk updates
~~~~~~~~~~~~

The `PositionManager` custom manager uses `PositionQuerySet` to provide a
`reposition` method that will update the position of all objects in the
queryset to match the current ordering.  If `reposition` is called on the
manager itself, all objects will be repositioned according to the default
model ordering.

Be aware that, unlike repositioning objects one at a time using list indices,
the `reposition` method will call the `save` method of every model instance
in the queryset.

Many-to-many
~~~~~~~~~~~~

Specifying a ``ManyToManyField`` as a ``collection`` won't work; use an
intermediate model with a ``PositionField`` instead::

    class Product(models.Model):
        name = models.CharField(max_length=50)

    class Category(models.Model):
        name = models.CharField(max_length=50)
        products = models.ManyToManyField(Product, through='ProductCategory', related_name='categories')

    class ProductCategory(models.Model):
        product = models.ForeignKey(Product)
        category = models.ForeignKey(Category)
        position = PositionField(collection='category')

        class Meta(object):
            unique_together = ('product', 'category')


Multi-table model inheritance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default, if a parent model has a position field that declares a collection,
child model instances are ordered independently. This behavior can be changed
by specifying a `parent_link` argument identifying the name of the one-to-one
field linking the child model to the parent. If `parent_link` is set, all subclass
instances will be part of a single sequence in each collection.


Limitations
-----------

* Unique constraints can't be applied to ``PositionField`` because they break
  the ability to update other items in a collection all at once.  This one was
  a bit painful, because setting the constraint is probably the right thing to
  do from a database consistency perspective, but the overhead in additional
  queries was too much to bear.

* After a position has been updated, other members of the collection are updated
  using a single SQL ``UPDATE`` statement, this means the ``save`` method of the
  other instances won't be called.  As a partial work-around to this issue,
  any ``DateTimeField`` with ``auto_now=True`` will be assigned the current time.


.. _`Django Positions needs a new maintainer.`: https://github.com/jpwatts/django-positions/issues/37
.. _`I`: http://joelwatts.com/
.. _`PyPI listing`: https://pypi.python.org/pypi/django-positions
.. _`Django`: http://www.djangoproject.com/
