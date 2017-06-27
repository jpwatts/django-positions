from unittest import skipIf
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
import django

from .models import MigrationTest

class MigrationTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @skipIf(django.VERSION < (1,7), 'Skipping migration test because Django < 1.7')
    def test_migration(self):
        # The data migration should have inserted the following record. This test just verifies that the data is there.
        # Ideally this test would run the migrations but setting up a data migration is faster for now.
        test = MigrationTest.objects.create(name="Some Person", age=37, favorite_color='Blue')
        result = list(MigrationTest.objects.order_by('position').values_list('name', 'age', 'favorite_color', 'position'))
        expected_result = [('Test Name', 99, 'Red', -1), ('Some Person', 37, 'Blue', 0)]
        self.assertEqual(result, expected_result)
