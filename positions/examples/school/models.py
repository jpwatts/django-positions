from django.db import models

from positions import PositionField


class SubUnit(models.Model):
    name = models.CharField(max_length=100)


class Task(models.Model):
    """
    Base class for lessons/exercises - ordered items within a sub-unit
    """
    sub_unit = models.ForeignKey(SubUnit)
    position = PositionField(collection='sub_unit')


class Lesson(Task):
    subject = models.CharField(max_length=100)
    text = models.TextField(blank=True)


class Exercise(Task):
    description = models.CharField(max_length=100)
