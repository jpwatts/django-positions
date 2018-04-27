from django.test import TestCase
import doctest
import unittest

from django.db import models

from examples.school.models import SubUnit, Lesson, Exercise


class SchoolsTestCase(TestCase):
    def setUp(self):
        self.american_revolution = SubUnit.objects.create(name="American Revolution")
        self.no_taxation = Lesson.objects.create(sub_unit=self.american_revolution, title="No Taxation without Representation", text="...")
        self.assertEqual(self.no_taxation.position, 0)

        self.research_paper = Exercise.objects.create(sub_unit=self.american_revolution, title="Paper", description="Two pages, double spaced")
        self.assertEqual(self.research_paper.position, 1)

        self.tea_party = Lesson.objects.create(sub_unit=self.american_revolution, title="Boston Tea Party", text="...")
        self.assertEqual(self.tea_party.position, 2)

        self.quiz = Exercise.objects.create(sub_unit=self.american_revolution, title="Pop Quiz", description="...")
        self.assertEqual(self.quiz.position, 3)

    def tearDown(self):
        SubUnit.objects.all().delete()

    @unittest.skip("This should not fail! Skipping during test development.")
    def test_explicit_position(self):
        # create a task with an explicit position
        self.intro_lesson = Lesson.objects.create(sub_unit=self.american_revolution, title="The Intro", text="...", position=0)
        actual_order = list(self.american_revolution.task_set.values_list('title', 'position'))
        expected_order = [
            (u'The Intro', 0),
            (u'No Taxation without Representation', 1),
            (u'Paper', 2),
            (u'Boston Tea Party', 3),
            (u'Pop Quiz', 4)
        ]
        self.assertEqual(actual_order, expected_order)