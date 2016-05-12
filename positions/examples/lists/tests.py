import time
import doctest
import unittest

from .models import List, Item

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
        self.l = List.objects.create(name='To Do')

        # create a couple items using the default position
        result = self.l.items.create(name='Write Tests').name
        expected_result = 'Write Tests'
        self.assertEqual(result, expected_result)

        result = list(self.l.items.values_list('name', 'position'))
        expected_result = [('Write Tests', 0)]
        self.assertEqual(result, expected_result)

        result = self.l.items.create(name='Exercise').name
        expected_result = 'Exercise'
        self.assertEqual(result, expected_result)

        result = list(self.l.items.values_list('name', 'position').order_by('position'))
        expected_result = [('Write Tests', 0), ('Exercise', 1)]
        self.assertEqual(result, expected_result)

        # create an item with an explicit position
        result = self.l.items.create(name='Learn to spell Exercise', position=0).name
        expected_result = 'Learn to spell Exercise'
        self.assertEqual(result, expected_result)

        result = list(self.l.items.values_list('name', 'position').order_by('position'))
        expected_result = [('Learn to spell Exercise', 0), ('Write Tests', 1), ('Exercise', 2)]
        self.assertEqual(result, expected_result)

        # save an item without changing it's position
        self.exercise = self.l.items.order_by('-position')[0]
        self.exercise.name = 'Exercise'
        self.exercise.save()

        result = list(self.l.items.values_list('name', 'position').order_by('position'))
        expected_result = [('Learn to spell Exercise', 0), ('Write Tests', 1), ('Exercise', 2)]
        self.assertEqual(result, expected_result)

        # delete an item
        self.learn_to_spell = self.l.items.order_by('position')[0]
        self.learn_to_spell.delete()

        result = list(self.l.items.values_list('name', 'position').order_by('position'))
        expected_result = [('Write Tests', 0), ('Exercise', 1)]
        self.assertEqual(result, expected_result)

        # create a couple more items
        result = self.l.items.create(name='Drink less Coke').name
        expected_result = 'Drink less Coke'
        self.assertEqual(result, expected_result)

        result = self.l.items.create(name='Go to Bed').name
        expected_result = 'Go to Bed'
        self.assertEqual(result, expected_result)

        result = list(self.l.items.values_list('name', 'position').order_by('position'))
        expected_result = [('Write Tests', 0), ('Exercise', 1), ('Drink less Coke', 2), ('Go to Bed', 3)]
        self.assertEqual(result, expected_result)

        # move item to end using None
        self.write_tests = self.l.items.order_by('position')[0]
        self.write_tests.position = None
        self.write_tests.save()
        result = list(self.l.items.values_list('name', 'position').order_by('position'))
        expected_result = [('Exercise', 0), ('Drink less Coke', 1), ('Go to Bed', 2), ('Write Tests', 3)]
        self.assertEqual(result, expected_result)

        # move item using negative index
        self.write_tests.position = -3
        self.write_tests.save()
        result = list(self.l.items.values_list('name', 'position').order_by('position'))
        expected_result = [('Exercise', 0), ('Write Tests', 1), ('Drink less Coke', 2), ('Go to Bed', 3)]
        self.assertEqual(result, expected_result)

        # move item to position
        self.write_tests.position = 2
        self.write_tests.save()

        result = list(self.l.items.values_list('name', 'position').order_by('position'))
        expected_result = [('Exercise', 0), ('Drink less Coke', 1), ('Write Tests', 2), ('Go to Bed', 3)]
        self.assertEqual(result, expected_result)

        # move item to beginning
        self.sleep = self.l.items.order_by('-position')[0]
        self.sleep.position = 0
        self.sleep.save()

        result = list(self.l.items.values_list('name', 'position').order_by('position'))
        expected_result = [('Go to Bed', 0), ('Exercise', 1), ('Drink less Coke', 2), ('Write Tests', 3)]
        self.assertEqual(result, expected_result)

        # check auto_now updates
        time.sleep(1)  # sleep to guarantee updated time increases
        sleep_updated, exercise_updated, eat_better_updated, write_tests_updated = [i.updated for i in self.l.items.all().order_by('position')]
        self.eat_better = self.l.items.all().order_by('-position')[1]
        self.eat_better.position = 1
        self.eat_better.save()
        time.sleep(1)  # sleep to guarantee updated time increases
        self.todo_list=list(self.l.items.all().order_by('position'))

        result = sleep_updated == self.todo_list[0].updated
        expected_result = True
        self.assertEqual(result, expected_result)

        result = eat_better_updated < self.todo_list[1].updated
        expected_result = True
        self.assertEqual(result, expected_result)

        result = exercise_updated < self.todo_list[2].updated
        expected_result = True
        self.assertEqual(result, expected_result)

        result = write_tests_updated == exercise_updated
        expected_result = True
        self.assertEqual(result, expected_result)

        # create an item using negative index
        # http://github.com/jpwatts/django-positions/issues/#issue/5
        result = list(self.l.items.values_list('name', 'position').order_by('position'))
        expected_result = [('Go to Bed', 0), ('Drink less Coke', 1), ('Exercise', 2), ('Write Tests', 3)]
        self.assertEqual(result, expected_result)

        self.fix_issue_5 = Item(list=self.l, name="Fix Issue #5")
        result = self.fix_issue_5.position
        expected_result = -1
        self.assertEqual(result, expected_result)

        self.fix_issue_5.position = -2
        result = self.fix_issue_5.position
        expected_result = -2
        self.assertEqual(result, expected_result)

        self.fix_issue_5.save()
        result = self.fix_issue_5.position
        expected_result = 3
        self.assertEqual(result, expected_result)

        result = list(self.l.items.values_list('name', 'position').order_by('position'))
        expected_result = [('Go to Bed', 0), ('Drink less Coke', 1), ('Exercise', 2), ('Fix Issue #5', 3), ('Write Tests', 4)]
        self.assertEqual(result, expected_result)

        # Try again, now that the model has been saved.
        self.fix_issue_5.position = -2
        self.fix_issue_5.save()
        result = self.fix_issue_5.position
        expected_result = 3
        self.assertEqual(result, expected_result)

        result = list(self.l.items.values_list('name', 'position').order_by('position'))
        expected_result = [('Go to Bed', 0), ('Drink less Coke', 1), ('Exercise', 2), ('Fix Issue #5', 3), ('Write Tests', 4)]
        self.assertEqual(result, expected_result)

        # create an item using with a position of zero
        # http://github.com/jpwatts/django-positions/issues#issue/7
        self.item0 = self.l.items.create(name="Fix Issue #7", position=0)
        result =  self.item0.position
        expected_result = 0
        self.assertEqual(result, expected_result)

        result = list(self.l.items.values_list('name', 'position').order_by('position'))
        expected_result = [('Fix Issue #7', 0), ('Go to Bed', 1), ('Drink less Coke', 2), ('Exercise', 3), ('Fix Issue #5', 4), ('Write Tests', 5)]
        self.assertEqual(result, expected_result)
