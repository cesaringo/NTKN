# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sce', '0004_auto_20150921_0543'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='grade_level',
            field=models.ForeignKey(null=True, verbose_name='Grade level', on_delete=django.db.models.deletion.SET_NULL, to='sce.GradeLevel', blank=True),
        ),
        migrations.AddField(
            model_name='course',
            name='level',
            field=models.IntegerField(null=True),
        ),
    ]
