from django.test import TestCase
import doctest
import unittest
import pprint
from positions.examples.photos.forms import PhotoForm
from positions.examples.photos.models import Album, Photo

class PhotosTestCase(TestCase):
    def setUp(self):
        self.album = Album.objects.create(name="Vacation")
        self.bahamas = self.album.photos.create(name="Bahamas")
        self.assertEqual(self.bahamas.position, 0)

        self.jamaica = self.album.photos.create(name="Jamaica")
        self.assertEqual(self.jamaica.position, 0)

        self.grand_cayman = self.album.photos.create(name="Grand Cayman")
        self.assertEqual(self.grand_cayman.position, 0)

        self.cozumel = self.album.photos.create(name="Cozumel")
        self.assertEqual(self.cozumel.position, 0)

    def tearDown(self):
        Album.objects.all().delete()

    def test_reordered_positions(self):
        ordered_by_position = list(self.album.photos.order_by('position').values_list('name', 'position'))
        expected_order = [(u'Cozumel', 0), (u'Grand Cayman', 1), (u'Jamaica', 2), (u'Bahamas', 3)]
        self.assertEqual(
            ordered_by_position,
            expected_order
        )

    @unittest.skip("Not sure if this should fail or not. Skipping until there is time to figure it out.")
    def test_renamed_positions(self):
        self.cozumel.name = "Cozumel, Mexico"
        self.cozumel.save(update_fields=['name'])

        self.jamaica.name = "Ocho Rios, Jamaica"
        self.jamaica.save(update_fields=['name', 'position'])
        self.assertEqual(self.jamaica.position, 1)

    @unittest.skip("Not sure if this should fail or not. Skipping until there is time to figure it out.")
    def test_form_renamed_position(self):
        grand_cayman_form = PhotoForm(dict(name="Georgetown, Grand Cayman"), instance=self.grand_cayman)
        grand_cayman_form.save()
        self.assertEqual(self.grand_cayman.position, 1)
