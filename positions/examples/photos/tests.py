import doctest
import unittest

from positions.examples.photos.forms import PhotoForm
from positions.examples.photos.models import Album, Photo


tests = """

>>> album = Album.objects.create(name="Vacation")


# The Photo model doesn't use the default (-1) position. Make sure that works.

>>> bahamas = album.photos.create(name="Bahamas")
>>> bahamas.position
0

>>> jamaica = album.photos.create(name="Jamaica")
>>> jamaica.position
0

>>> grand_cayman = album.photos.create(name="Grand Cayman")
>>> grand_cayman.position
0

>>> cozumel = album.photos.create(name="Cozumel")
>>> cozumel.position
0

>>> album.photos.order_by('position').values_list('name', 'position')
[(u'Cozumel', 0), (u'Grand Cayman', 1), (u'Jamaica', 2), (u'Bahamas', 3)]

>>> cozumel.name = "Cozumel, Mexico"
>>> cozumel.save(update_fields=['name'])
>>> cozumel.position
0

>>> jamaica.name = "Ocho Rios, Jamaica"
>>> jamaica.save(update_fields=['name', 'position'])
>>> jamaica.position
2

>>> grand_cayman_form = PhotoForm(dict(name="Georgetown, Grand Cayman"), instance=grand_cayman)
>>> grand_cayman = grand_cayman_form.save()
>>> grand_cayman.position
1

"""


__test__ = {'tests': tests}


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite())
    return tests
