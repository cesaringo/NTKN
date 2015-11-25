# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alumni', '0003_auto_20151120_2323'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='first_school_year',
        ),
        migrations.DeleteModel(
            name='SchoolYear',
        ),
    ]
