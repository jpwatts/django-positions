import doctest
import unittest

from django.contrib.contenttypes.models import ContentType

from positions.examples.lists.models import List
from positions.examples.generic.models import GenericThing

from django.test import TestCase

class GenericTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        GenericThing.objects.all().delete()
        ContentType.objects.all().delete()
        List.objects.all().delete()

    # @unittest.skip("Some reason. If you are reading this in a test run someone did not fill this in.")
    def test_doctests_standin(self):
        # This code just contains the old doctests for this module. They should be most likely split out into their own
        # tests at some point.
        self.l = List.objects.create(name='To Do')
        self.ct = ContentType.objects.get_for_model(self.l)
        self.t1 = GenericThing.objects.create(name="First Generic Thing", object_id=self.l.pk, content_type=self.ct)

        self.t2 = GenericThing.objects.create(name="Second Generic Thing", object_id=self.l.pk, content_type=self.ct)
        self.assertEquals(self.t1.position, 0)
        self.assertEquals(self.t2.position, 1)
        self.t1.position = 1
        self.t1.save()

        self.assertEquals(self.t1.position, 1)
        self.t2 = GenericThing.objects.get(pk=2)
        self.assertEquals(self.t2.position, 0)
        self.t1.delete()

        actual_order = list(GenericThing.objects.filter(object_id=self.l.pk, content_type=self.ct).values_list('name', 'position').order_by('position'))
        expected_order = [(u'Second Generic Thing', 0)]
        self.assertEqual(actual_order, expected_order)
        self.t3 = GenericThing.objects.create(object_id=self.l.pk, content_type=self.ct, name='Mr. None')
        self.t3.save()
        self.assertEquals(self.t3.position, 1)
        self.t4 = GenericThing.objects.create(object_id=self.l.pk, content_type=self.ct, name='Mrs. None')
        self.assertEquals(self.t4.position, 2)
        self.t4.position = -2
        self.t4.save()
        self.assertEquals(self.t4.position, 1)
        actual_order = list(GenericThing.objects.order_by('position').values_list('name', flat=True))
        expected_order = [u'Second Generic Thing', u'Mrs. None', u'Mr. None']
        self.assertEqual(actual_order, expected_order)
