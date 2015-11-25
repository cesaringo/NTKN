# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alumni', '0006_auto_20151123_2334'),
        ('sce', '0008_auto_20151123_2334'),
    ]

    operations = [
        migrations.DeleteModel(
            name='EducativeProgram',
        ),
    ]
