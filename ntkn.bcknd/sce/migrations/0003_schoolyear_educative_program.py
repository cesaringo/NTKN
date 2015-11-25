# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alumni', '0002_auto_20151114_0929'),
        ('sce', '0002_auto_20151114_0929'),
    ]

    operations = [
        migrations.AddField(
            model_name='schoolyear',
            name='educative_program',
            field=models.ForeignKey(default=2, to='alumni.EducativeProgram'),
            preserve_default=False,
        ),
    ]
