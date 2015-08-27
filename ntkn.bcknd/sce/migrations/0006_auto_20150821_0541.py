# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sce', '0005_auto_20150821_0439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='fullname',
            field=models.CharField(max_length=255, verbose_name='Subject Name'),
        ),
    ]
