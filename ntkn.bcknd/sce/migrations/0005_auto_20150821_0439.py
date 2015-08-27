# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sce', '0004_auto_20150821_0438'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subjectcategory',
            name='order',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
