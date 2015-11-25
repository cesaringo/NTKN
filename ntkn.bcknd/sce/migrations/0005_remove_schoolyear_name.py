# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sce', '0004_auto_20151119_2307'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schoolyear',
            name='name',
        ),
    ]
