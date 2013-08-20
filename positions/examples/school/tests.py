from django.db import models

from positions.examples.school.models import SubUnit, Lesson, Exercise


tests = """

>>> american_revolution = SubUnit.objects.create(name="American Revolution")

>>> no_taxation = Lesson.objects.create(sub_unit=american_revolution, subject="No Taxation without Representation")
>>> no_taxation.position
0

>>> research_paper = Exercise.objects.create(sub_unit=american_revolution, description="Two pages, double spaced")
>>> research_paper.position
1

>>> tea_party = Lesson.objects.create(sub_unit=american_revolution, subject="Boston Tea Party")
>>> tea_party.position
2

"""


__test__ = {'tests': tests}
