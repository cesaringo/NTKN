# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alumni', '0002_auto_20151110_0120'),
    ]

    operations = [
        migrations.RenameField(
            model_name='educativeprogram',
            old_name='marking_periods',
            new_name='num_marking_periods',
        ),
    ]
