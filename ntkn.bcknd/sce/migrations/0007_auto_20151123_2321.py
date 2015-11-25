# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sce', '0006_schoolyear_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='educative_program',
            field=models.ForeignKey(to='alumni.EducativeProgram', default=''),
            preserve_default=False,
        ),
    ]
