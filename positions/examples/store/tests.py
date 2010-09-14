from django.db import models

from positions import PositionField
from positions.examples.store.models import Product, Category, ProductCategory


tests = """

>>> clothes = Category.objects.create(name="Clothes")
>>> sporting_goods = Category.objects.create(name="Sporting Goods")

>>> bat = Product.objects.create(name="Bat")
>>> bat_in_sporting_goods = ProductCategory.objects.create(product=bat, category=sporting_goods)

>>> cap = Product.objects.create(name="Cap")
>>> cap_in_sporting_goods = ProductCategory.objects.create(product=cap, category=sporting_goods)
>>> cap_in_clothes = ProductCategory.objects.create(product=cap, category=clothes)

>>> glove = Product.objects.create(name="Glove")
>>> glove_in_sporting_goods = ProductCategory.objects.create(product=glove, category=sporting_goods)

>>> tshirt = Product.objects.create(name="T-shirt")
>>> tshirt_in_clothes = ProductCategory.objects.create(product=tshirt, category=clothes)

>>> jeans = Product.objects.create(name="Jeans")
>>> jeans_in_clothes = ProductCategory.objects.create(product=jeans, category=clothes)

>>> jersey = Product.objects.create(name="Jersey")
>>> jersey_in_sporting_goods = ProductCategory.objects.create(product=jersey, category=sporting_goods)
>>> jersey_in_clothes = ProductCategory.objects.create(product=jersey, category=clothes)

>>> ball = Product.objects.create(name="Ball")
>>> ball_in_sporting_goods = ProductCategory.objects.create(product=ball, category=sporting_goods)

>>> ProductCategory.objects.filter(category=clothes).values_list('product__name', 'position').order_by('position')
[(u'Cap', 0), (u'T-shirt', 1), (u'Jeans', 2), (u'Jersey', 3)]

>>> ProductCategory.objects.filter(category=sporting_goods).values_list('product__name', 'position').order_by('position')
[(u'Bat', 0), (u'Cap', 1), (u'Glove', 2), (u'Jersey', 3), (u'Ball', 4)]


Moving cap in sporting goods shouldn't effect its position in clothes.

>>> cap_in_sporting_goods.position = -1
>>> cap_in_sporting_goods.save()

>>> ProductCategory.objects.filter(category=clothes).values_list('product__name', 'position').order_by('position')
[(u'Cap', 0), (u'T-shirt', 1), (u'Jeans', 2), (u'Jersey', 3)]

>>> ProductCategory.objects.filter(category=sporting_goods).values_list('product__name', 'position').order_by('position')
[(u'Bat', 0), (u'Glove', 1), (u'Jersey', 2), (u'Ball', 3), (u'Cap', 4)]


# Deleting an object should reorder both collections.
>>> cap.delete()

>>> ProductCategory.objects.filter(category=clothes).values_list('product__name', 'position').order_by('position')
[(u'T-shirt', 0), (u'Jeans', 1), (u'Jersey', 2)]

>>> ProductCategory.objects.filter(category=sporting_goods).values_list('product__name', 'position').order_by('position')
[(u'Bat', 0), (u'Glove', 1), (u'Jersey', 2), (u'Ball', 3)]

"""


__test__ = {'tests': tests}
