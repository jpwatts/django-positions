# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import positions.fields


class Migration(migrations.Migration):

    dependencies = [
        ('migration', '0002_insert_test_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='migrationtest',
            name='position',
            field=positions.fields.PositionField(default=-1),
            preserve_default=True,
        ),
    ]
