from django.db import models

from positions.examples.school.models import SubUnit, Lesson, Exercise


tests = """

>>> american_revolution = SubUnit.objects.create(name="American Revolution")

>>> no_taxation = Lesson.objects.create(sub_unit=american_revolution, title="No Taxation without Representation", text="...")
>>> no_taxation.position
0

>>> research_paper = Exercise.objects.create(sub_unit=american_revolution, title="Paper", description="Two pages, double spaced")
>>> research_paper.position
1

>>> tea_party = Lesson.objects.create(sub_unit=american_revolution, title="Boston Tea Party", text="...")
>>> tea_party.position
2

>>> quiz = Exercise.objects.create(sub_unit=american_revolution, title="Pop Quiz", description="...")
>>> quiz.position
3

# create a task with an explicit position
>>> intro_lesson = Lesson.objects.create(sub_unit=american_revolution, title="The Intro", text="...", position=0)
>>> american_revolution.task_set.values_list('title', 'position')
[(u'The Intro', 0), (u'No Taxation without Representation', 1), (u'Paper', 2), (u'Boston Tea Party', 3)]
"""


__test__ = {'tests': tests}
