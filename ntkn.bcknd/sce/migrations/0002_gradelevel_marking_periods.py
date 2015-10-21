# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sce', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='gradelevel',
            name='marking_periods',
            field=models.IntegerField(default=5),
            preserve_default=False,
        ),
    ]
