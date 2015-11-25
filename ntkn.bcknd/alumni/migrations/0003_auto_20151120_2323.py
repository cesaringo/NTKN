# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alumni', '0002_auto_20151114_0929'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schoolyear',
            name='name',
            field=models.CharField(null=True, blank=True, max_length=100),
        ),
    ]
