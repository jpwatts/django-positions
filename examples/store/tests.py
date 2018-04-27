import doctest
import unittest

from django.db import models

from positions import PositionField
from examples.store.models import Product, Category, ProductCategory

from django.test import TestCase

class StoreTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        Category.objects.all().delete()
        Product.objects.all().delete()
        ProductCategory.objects.all().delete()

    # @unittest.skip("Some reason. If you are reading this in a test run someone did not fill this in.")
    def test_doctests_standin(self):
        # This code just contains the old doctests for this module. They should be most likely split out into their own
        # tests at some point.
        self.clothes = Category.objects.create(name="Clothes")
        self.sporting_goods = Category.objects.create(name="Sporting Goods")

        self.bat = Product.objects.create(name="Bat")
        self.bat_in_sporting_goods = ProductCategory.objects.create(product=self.bat, category=self.sporting_goods)

        self.cap = Product.objects.create(name="Cap")
        self.cap_in_sporting_goods = ProductCategory.objects.create(product=self.cap, category=self.sporting_goods)
        self.cap_in_clothes = ProductCategory.objects.create(product=self.cap, category=self.clothes)

        self.glove = Product.objects.create(name="Glove")
        self.glove_in_sporting_goods = ProductCategory.objects.create(product=self.glove, category=self.sporting_goods)

        self.tshirt = Product.objects.create(name="T-shirt")
        self.tshirt_in_clothes = ProductCategory.objects.create(product=self.tshirt, category=self.clothes)

        self.jeans = Product.objects.create(name="Jeans")
        self.jeans_in_clothes = ProductCategory.objects.create(product=self.jeans, category=self.clothes)

        self.jersey = Product.objects.create(name="Jersey")
        self.jersey_in_sporting_goods = ProductCategory.objects.create(product=self.jersey, category=self.sporting_goods)
        self.jersey_in_clothes = ProductCategory.objects.create(product=self.jersey, category=self.clothes)

        self.ball = Product.objects.create(name="Ball")
        self.ball_in_sporting_goods = ProductCategory.objects.create(product=self.ball, category=self.sporting_goods)

        actual_order = list(ProductCategory.objects.filter(category=self.clothes).values_list('product__name', 'position').order_by('position'))
        expected_order = [(u'Cap', 0), (u'T-shirt', 1), (u'Jeans', 2), (u'Jersey', 3)]
        self.assertEqual(actual_order, expected_order)

        actual_order = list(ProductCategory.objects.filter(category=self.sporting_goods).values_list('product__name', 'position').order_by('position'))
        expected_order = [(u'Bat', 0), (u'Cap', 1), (u'Glove', 2), (u'Jersey', 3), (u'Ball', 4)]
        self.assertEqual(actual_order, expected_order)

        # Moving cap in sporting goods shouldn't effect its position in clothes.

        self.cap_in_sporting_goods.position = -1
        self.cap_in_sporting_goods.save()

        actual_order = list(ProductCategory.objects.filter(category=self.clothes).values_list('product__name', 'position').order_by('position'))
        expected_order = [(u'Cap', 0), (u'T-shirt', 1), (u'Jeans', 2), (u'Jersey', 3)]
        self.assertEqual(actual_order, expected_order)

        actual_order = list(ProductCategory.objects.filter(category=self.sporting_goods).values_list('product__name', 'position').order_by('position'))
        expected_order = [(u'Bat', 0), (u'Glove', 1), (u'Jersey', 2), (u'Ball', 3), (u'Cap', 4)]
        self.assertEqual(actual_order, expected_order)

        # Deleting an object should reorder both collections.
        self.cap.delete()

        actual_order = list(ProductCategory.objects.filter(category=self.clothes).values_list('product__name', 'position').order_by('position'))
        expected_order = [(u'T-shirt', 0), (u'Jeans', 1), (u'Jersey', 2)]
        self.assertEqual(actual_order, expected_order)

        actual_order = list(ProductCategory.objects.filter(category=self.sporting_goods).values_list('product__name', 'position').order_by('position'))
        expected_order = [(u'Bat', 0), (u'Glove', 1), (u'Jersey', 2), (u'Ball', 3)]
        self.assertEqual(actual_order, expected_order)
