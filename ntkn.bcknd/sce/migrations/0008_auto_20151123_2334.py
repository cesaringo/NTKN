# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alumni', '0006_auto_20151123_2334'),
        ('sce', '0007_auto_20151123_2321'),
    ]

    operations = [
        migrations.CreateModel(
            name='EducativeProgram',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('slug', models.CharField(blank=True, unique=True, max_length=100)),
                ('num_marking_periods', models.IntegerField()),
                ('num_of_levels', models.IntegerField()),
                ('is_active', models.BooleanField(default=True)),
                ('order', models.IntegerField(null=True, blank=True)),
                ('institute', models.ForeignKey(to='alumni.Institute')),
            ],
        ),
        migrations.AlterField(
            model_name='markingperiod',
            name='educative_program',
            field=models.ForeignKey(to='sce.EducativeProgram'),
        ),
        migrations.AlterField(
            model_name='schoolyear',
            name='educative_program',
            field=models.ForeignKey(to='sce.EducativeProgram'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='educative_program',
            field=models.ForeignKey(to='sce.EducativeProgram'),
        ),
    ]
