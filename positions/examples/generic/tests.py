from django.contrib.contenttypes.models import ContentType

from positions.examples.lists.models import List
from positions.examples.generic.models import GenericThing

tests = """
>>> l = List.objects.create(name='To Do')
>>> ct = ContentType.objects.get_for_model(l)
>>> t1 = GenericThing.objects.create(name="First Generic Thing",
...                                  object_id=l.pk,
...                                  content_type=ct)

>>> t2 = GenericThing.objects.create(name="Second Generic Thing",
...                                  object_id=l.pk,
...                                  content_type=ct)
>>> t1.position
0
>>> t2.position
1
>>> t1.position = 1
>>> t1.save()

>>> t1.position
1
>>> t2 = GenericThing.objects.get(pk=2)
>>> t2.position
0
>>> t1.delete()

>>> GenericThing.objects.filter(object_id=l.pk, content_type=ct).values_list('name', 'position').order_by('position')
[(u'Second Generic Thing', 0)]
>>> t3 = GenericThing.objects.create(object_id=l.pk, content_type=ct, name='Mr. None')
>>> t3.save()
>>> t3.position
1
>>> t4 = GenericThing.objects.create(object_id=l.pk, content_type=ct, name='Mrs. None')
>>> t4.position
2
>>> t4.position = -2
>>> t4.save()
>>> t4.position
1
>>> GenericThing.objects.order_by('position').values_list('name', flat=True)
[u'Second Generic Thing', u'Mrs. None', u'Mr. None']
"""


__test__ = {'tests': tests}
