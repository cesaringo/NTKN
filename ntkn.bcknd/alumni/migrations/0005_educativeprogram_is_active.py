# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alumni', '0004_auto_20151121_1138'),
    ]

    operations = [
        migrations.AddField(
            model_name='educativeprogram',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
