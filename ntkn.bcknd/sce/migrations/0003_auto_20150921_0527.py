# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sce', '0002_gradelevel_marking_periods'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gradelevel',
            name='marking_periods',
        ),
        migrations.AddField(
            model_name='educativeprogram',
            name='marking_periods',
            field=models.IntegerField(default=5),
            preserve_default=False,
        ),
    ]
