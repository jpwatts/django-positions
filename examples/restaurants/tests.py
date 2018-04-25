import doctest
import unittest

from django.db import models

from examples.restaurants.models import Menu, Food, Drink

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
        self.romanos = Menu.objects.create(name="Romano's Pizza")

        self.pizza = Food.objects.create(menu=self.romanos, name="Pepperoni")
        result = self.pizza.position
        expected_result = 0
        self.assertEqual(result, expected_result)

        self.wine = Drink.objects.create(menu=self.romanos, name="Merlot")
        result = self.wine.position
        expected_result = 0
        self.assertEqual(result, expected_result)

        self.spaghetti = Food.objects.create(menu=self.romanos, name="Spaghetti & Meatballs")
        result = self.spaghetti.position
        expected_result = 1
        self.assertEqual(result, expected_result)

        self.soda = Drink.objects.create(menu=self.romanos, name="Coca-Cola")
        result = self.soda.position
        expected_result = 1
        self.assertEqual(result, expected_result)
