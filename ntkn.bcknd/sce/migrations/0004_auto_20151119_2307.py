# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sce', '0003_schoolyear_educative_program'),
    ]

    operations = [
        migrations.RenameField(
            model_name='schoolyear',
            old_name='active_year',
            new_name='is_active',
        ),
    ]
