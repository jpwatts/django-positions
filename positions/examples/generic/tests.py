from django.contrib.contenttypes.models import ContentType

from positions.examples.lists.models import List
from positions.examples.generic.models import GenericThing

tests="""
>>> l = List.objects.create(name='To Do')
>>> t1=GenericThing.objects.create(name="First Generic Thing",
...                                object_id=l.pk,
...                                content_type=ContentType.objects.get_for_model(l))

>>> t2=GenericThing.objects.create(name="Second Generic Thing",
...                                object_id=l.pk,
...                                content_type=ContentType.objects.get_for_model(l))
>>> t1.position
0
>>> t2.position
1
>>> t1.position=1
>>> t1.save()

>>> t1.position
1
>>> t2=GenericThing.objects.get(pk=2)
>>> t2.position
0
"""
__test__ = {'tests': tests}
