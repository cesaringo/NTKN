# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sce', '0007_educativeprogram_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='cohorts',
        ),
        migrations.AlterField(
            model_name='student',
            name='parent_email',
            field=models.EmailField(max_length=254, blank=True),
        ),
    ]
