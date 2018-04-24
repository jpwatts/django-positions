from django.db import models

from positions import PositionField


class SubUnit(models.Model):
    name = models.CharField(max_length=100)


class Task(models.Model):
    """
    Base class for lessons/exercises - ordered items within a sub-unit
    """
    sub_unit = models.ForeignKey(SubUnit, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    position = PositionField(collection='sub_unit', parent_link='task_ptr')


class Lesson(Task):
    text = models.CharField(max_length=100)


class Exercise(Task):
    description = models.CharField(max_length=100)
