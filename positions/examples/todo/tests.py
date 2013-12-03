import doctest
import unittest

from positions.examples.todo import models


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(models))
    return tests
