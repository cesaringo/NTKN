# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sce', '0005_auto_20150923_0418'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='grade_level',
        ),
        migrations.RemoveField(
            model_name='course',
            name='level',
        ),
    ]
