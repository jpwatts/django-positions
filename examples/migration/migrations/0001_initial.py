# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MigrationTest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=80)),
                ('age', models.IntegerField(null=True, blank=True)),
                ('favorite_color', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
