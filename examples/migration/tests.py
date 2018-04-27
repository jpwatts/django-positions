from unittest import skipIf
from .models import MigrationTest
from django.test import TestCase
import django


class MigrationTestCase(TestCase):
    @skipIf(django.VERSION < (1,7), 'Skipping migration test because Django < 1.7')
    def test_migration(self):
        # The data migration should have inserted the following record. This test just verifies that the data is there.
        # Ideally this test would run the migrations but setting up a data migration is faster for now.
        test = MigrationTest.objects.create(name="Some Person", age=37, favorite_color='Blue')
        result = list(MigrationTest.objects.order_by('position').values_list('name', 'age', 'favorite_color', 'position'))
        expected_result = [(u'Test Name', 99, u'Red', -1), (u'Some Person', 37, u'Blue', 0)]
        self.assertEqual(result, expected_result)
