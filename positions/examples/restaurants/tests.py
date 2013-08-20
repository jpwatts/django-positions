from django.db import models

from positions.examples.restaurants.models import Menu, Food, Drink


tests = """

>>> romanos = Menu.objects.create(name="Romano's Pizza")

>>> pizza = Food.objects.create(menu=romanos, name="Pepperoni")
>>> pizza.position
0

>>> wine = Drink.objects.create(menu=romanos, name="Merlot")
>>> wine.position
0

>>> spaghetti = Food.objects.create(menu=romanos, name="Spaghetti & Meatballs")
>>> spaghetti.position
1

>>> soda = Drink.objects.create(menu=romanos, name="Coca-Cola")
>>> soda.position
1

"""


__test__ = {'tests': tests}
