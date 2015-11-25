# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sce', '0005_remove_schoolyear_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='schoolyear',
            name='slug',
            field=models.CharField(max_length=100, blank=True, unique=True),
        ),
    ]
