# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sce', '0002_subject_levels'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='order',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='subject',
            name='fullname',
            field=models.CharField(verbose_name='Subject Name', unique=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='subject',
            name='shortname',
            field=models.CharField(verbose_name='Key', max_length=255),
        ),
    ]
