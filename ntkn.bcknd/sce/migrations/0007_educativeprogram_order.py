# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sce', '0006_auto_20150821_0541'),
    ]

    operations = [
        migrations.AddField(
            model_name='educativeprogram',
            name='order',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
