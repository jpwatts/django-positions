from django.db import models

import positions


class Item(models.Model):
    description = models.CharField(max_length=50)
    position = positions.PositionField()

    objects = positions.PositionManager()

    def __unicode__(self):
        return self.description


__test__ = {'API_TESTS':"""

>>> Item.objects.create(description="Add a `reposition` method")
<Item: Add a `reposition` method>

>>> Item.objects.create(description="Write some tests")
<Item: Write some tests>

>>> Item.objects.create(description="Push to GitHub")
<Item: Push to GitHub>

>>> Item.objects.order_by('position')
[<Item: Add a `reposition` method>, <Item: Write some tests>, <Item: Push to GitHub>]

>>> alphabetized = Item.objects.order_by('description')
>>> alphabetized
[<Item: Add a `reposition` method>, <Item: Push to GitHub>, <Item: Write some tests>]

>>> repositioned = alphabetized.reposition(save=False)
>>> repositioned
[<Item: Add a `reposition` method>, <Item: Push to GitHub>, <Item: Write some tests>]

# Make sure the position wasn't saved
>>> Item.objects.order_by('position')
[<Item: Add a `reposition` method>, <Item: Write some tests>, <Item: Push to GitHub>]

>>> repositioned = alphabetized.reposition()
>>> repositioned
[<Item: Add a `reposition` method>, <Item: Push to GitHub>, <Item: Write some tests>]

>>> Item.objects.order_by('position')
[<Item: Add a `reposition` method>, <Item: Push to GitHub>, <Item: Write some tests>]

>>> item = Item.objects.order_by('position')[0]
>>> item
<Item: Add a `reposition` method>

>>> item.position
0

>>> item.position = -1
>>> item.save()

# Make sure the signals are still connected
>>> Item.objects.order_by('position')
[<Item: Push to GitHub>, <Item: Write some tests>, <Item: Add a `reposition` method>]

>>> [i.position for i in Item.objects.order_by('position')]
[0, 1, 2]


# Add an item at position zero
# http://github.com/jpwatts/django-positions/issues/#issue/7

>>> item0 = Item(description="Fix Issue #7")
>>> item0.position = 0
>>> item0.save()

>>> Item.objects.values_list('description', 'position').order_by('position')
[(u'Fix Issue #7', 0), (u'Push to GitHub', 1), (u'Write some tests', 2), (u'Add a `reposition` method', 3)]

"""}
