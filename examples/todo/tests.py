import doctest
import unittest

from examples.todo.models import Item

from django.test import TestCase

class GenericTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    # @unittest.skip("Some reason. If you are reading this in a test run someone did not fill this in.")
    def test_doctests_standin(self):
        # This code just contains the old doctests for this module. They should be most likely split out into their own
        # tests at some point.
        result = Item.objects.position_field_name
        expected_result = 'index'
        self.assertEqual(result, expected_result)

        result = Item.objects.all().position_field_name
        expected_result = 'index'
        self.assertEqual(result, expected_result)

        result = Item.objects.create(description="Add a `reposition` method").description
        expected_result = 'Add a `reposition` method'
        self.assertEqual(result, expected_result)

        result = Item.objects.create(description="Write some tests").description
        expected_result = 'Write some tests'
        self.assertEqual(result, expected_result)

        result = Item.objects.create(description="Push to GitHub").description
        expected_result =  'Push to GitHub'
        self.assertEqual(result, expected_result)

        result =  list(Item.objects.order_by('index').values_list('description'))
        expected_result = [(u'Add a `reposition` method',), (u'Write some tests',), (u'Push to GitHub',)]
        self.assertEqual(result, expected_result)

        self.alphabetized = Item.objects.order_by('description')
        result = list(self.alphabetized.values_list('description'))
        expected_result = [(u'Add a `reposition` method',), (u'Push to GitHub',), (u'Write some tests',)]
        self.assertEqual(result, expected_result)

        result = self.alphabetized.position_field_name
        expected_result = 'index'
        self.assertEqual(result, expected_result)

        self.repositioned = self.alphabetized.reposition(save=False)
        result = list(self.repositioned.values_list('description'))
        expected_result = [(u'Add a `reposition` method',), (u'Push to GitHub',), (u'Write some tests',)]
        self.assertEqual(result, expected_result)

        # Make sure the position wasn't saved
        result = list(Item.objects.order_by('index').values_list('description'))
        expected_result = [(u'Add a `reposition` method',), (u'Write some tests',), (u'Push to GitHub',)]
        self.assertEqual(result, expected_result)

        self.repositioned = self.alphabetized.reposition()
        result = list(self.repositioned.values_list('description'))
        expected_result = [(u'Add a `reposition` method',), (u'Push to GitHub',), (u'Write some tests',)]
        self.assertEqual(result, expected_result)

        result = list(Item.objects.order_by('index').values_list('description'))
        expected_result = [(u'Add a `reposition` method',), (u'Push to GitHub',), (u'Write some tests',)]
        self.assertEqual(result, expected_result)

        self.item = Item.objects.order_by('index')[0]
        result = self.item.description
        expected_result = 'Add a `reposition` method'
        self.assertEqual(result, expected_result)

        result = self.item.index
        expected_result = 0

        self.item.index = -1
        self.item.save()

        # Make sure the signals are still connected
        result = list(Item.objects.order_by('index').values_list('description'))
        expected_result = [(u'Push to GitHub',), (u'Write some tests',), (u'Add a `reposition` method',)]
        self.assertEqual(result, expected_result)

        result = [i.index for i in Item.objects.order_by('index')]
        expected_result = [0, 1, 2]
        self.assertEqual(result, expected_result)


        # Add an item at position zero
        # http://github.com/jpwatts/django-positions/issues/#issue/7

        self.item0 = Item(description="Fix Issue #7")
        self.item0.index = 0
        self.item0.save()

        result = list(Item.objects.values_list('description', 'index').order_by('index'))
        expected_result = [(u'Fix Issue #7', 0), (u'Push to GitHub', 1), (u'Write some tests', 2), (u'Add a `reposition` method', 3)]
        self.assertEqual(result, expected_result)
