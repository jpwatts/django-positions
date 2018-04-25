from django.test import TestCase
import doctest
import unittest
import pprint
from examples.photos.forms import PhotoForm
from examples.photos.models import Album, Photo

class PhotosTestCase(TestCase):
    def setUp(self):
        self.album = Album.objects.create(name="Vacation")
        self.bahamas = self.album.photos.create(name="Bahamas")
        self.bahamas_id = self.bahamas.id
        self.assertEqual(self.bahamas.position, 0)

        self.jamaica = self.album.photos.create(name="Jamaica")
        self.jamaica_id = self.jamaica.id
        self.assertEqual(self.jamaica.position, 0)

        self.grand_cayman = self.album.photos.create(name="Grand Cayman")
        self.grand_cayman_id = self.grand_cayman.id
        self.assertEqual(self.grand_cayman.position, 0)

        self.cozumel = self.album.photos.create(name="Cozumel")
        self.cozumel_id = self.cozumel.id
        self.assertEqual(self.cozumel.position, 0)

    def refresh(self):
        self.bahamas = Photo.objects.get(id=self.bahamas_id)
        self.jamaica = Photo.objects.get(id=self.jamaica_id)
        self.grand_cayman = Photo.objects.get(id=self.grand_cayman_id)
        self.cozumel = Photo.objects.get(id=self.cozumel_id)

    def tearDown(self):
        Album.objects.all().delete()

    def test_reordered_positions(self):
        ordered_by_position = list(self.album.photos.order_by('position').values_list('name', 'position'))
        expected_order = [(u'Cozumel', 0), (u'Grand Cayman', 1), (u'Jamaica', 2), (u'Bahamas', 3)]
        self.assertEqual(
            ordered_by_position,
            expected_order
        )

    def test_renamed_positions(self):
        self.refresh()
        new_name = 'Cozumel, Mexico'
        self.cozumel.name = new_name
        self.cozumel.save(update_fields=['name'])
        self.refresh()
        self.assertEqual(self.cozumel.name, new_name)
        self.assertEqual(self.cozumel.position, 0)

        self.jamaica.name = "Ocho Rios, Jamaica"
        self.jamaica.save(update_fields=['name', 'position'])
        self.refresh()
        self.assertEqual(self.jamaica.position, 2)

        self.jamaica.position = -1
        self.jamaica.save(update_fields=['name', 'position'])
        self.refresh()
        self.assertEqual(self.jamaica.position, 3)

    def test_form_renamed_position(self):
        self.refresh()
        grand_cayman_form = PhotoForm(dict(name="Georgetown, Grand Cayman"), instance=self.grand_cayman)
        grand_cayman_form.save()
        self.refresh()
        self.assertEqual(self.grand_cayman.position, 1)
