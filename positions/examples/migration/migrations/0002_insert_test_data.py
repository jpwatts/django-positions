# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import positions.fields


def add_test_data(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    MigrationTest = apps.get_model("migration", "MigrationTest")
    test_record = MigrationTest.objects.create(name='Test Name', age=99, favorite_color='Red')

class Migration(migrations.Migration):

    dependencies = [
        ('migration', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_test_data),
    ]


