# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alumni', '0005_educativeprogram_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='educativeprogram',
            name='institute',
        ),
        migrations.AlterField(
            model_name='gradelevel',
            name='educative_program',
            field=models.ForeignKey(to='sce.EducativeProgram'),
        ),
    ]
