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

"""


__test__ = {'tests': tests}
