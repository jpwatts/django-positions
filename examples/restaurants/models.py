from django.db import models

from positions import PositionField


class Menu(models.Model):
    name = models.CharField(max_length=100)


class Item(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    position = PositionField(collection='menu')


class Food(Item):
    name = models.CharField(max_length=100)


class Drink(Item):
    name = models.CharField(max_length=100)
