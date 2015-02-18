import doctest
import unittest
from models import MigrationTest
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase


class MigrationTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_migration(self):
        # The data migration should have inserted the following record. This test just verifies that the data is there.
        # Ideally this test would run the migrations but setting up a data migration is faster for now.
        test = MigrationTest.objects.create(name="Some Person", age=37, favorite_color='Blue')
        result = list(MigrationTest.objects.order_by('position').values_list('name', 'age', 'favorite_color', 'position'))
        expected_result = [(u'Test Name', 99, u'Red', -1), (u'Some Person', 37, u'Blue', 0)]
        self.assertEqual(result, expected_result)