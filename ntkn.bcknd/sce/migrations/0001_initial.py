# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import datetime
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('alumni', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('cohort', models.ForeignKey(to='alumni.Cohort')),
            ],
        ),
        migrations.CreateModel(
            name='CourseEnrollment',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('course', models.ForeignKey(to='sce.Course')),
                ('student', models.ForeignKey(to='alumni.Student')),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(unique=True, verbose_name='Department Name', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='MarkingPeriod',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(unique=True, max_length=255)),
                ('shortname', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('grades_due', models.DateField(validators=[django.core.validators.MinValueValidator(datetime.date(1970, 1, 1))], blank=True, null=True, help_text='If filled out, teachers will be notified when grades are due.')),
                ('active', models.BooleanField(default=False, help_text='Teachers may only enter grades for active marking periods. There may be more than one active marking period.')),
                ('educative_program', models.ForeignKey(to='alumni.EducativeProgram')),
            ],
            options={
                'ordering': ('shortname',),
            },
        ),
        migrations.CreateModel(
            name='SchoolYear',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(unique=True, max_length=100)),
                ('start_date', models.DateField(validators=[django.core.validators.MinValueValidator(datetime.date(1970, 1, 1))])),
                ('end_date', models.DateField(validators=[django.core.validators.MinValueValidator(datetime.date(1970, 1, 1))])),
                ('active_year', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('start_date',),
            },
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('score', models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(10.0)])),
                ('course_enrollment', models.ForeignKey(related_name='scores', related_query_name='score', to='sce.CourseEnrollment')),
                ('marking_period', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='sce.MarkingPeriod', null=True)),
            ],
            options={
                'ordering': ('marking_period',),
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('fullname', models.CharField(verbose_name='Subject Name', max_length=255)),
                ('shortname', models.CharField(verbose_name='Key', max_length=255)),
                ('graded', models.BooleanField(default=True, help_text='Teachers can submit grades for this course')),
                ('description', models.TextField(blank=True, null=True)),
                ('level', models.IntegerField(null=True)),
                ('order', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubjectCategory',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('order', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='subject',
            name='category',
            field=models.ForeignKey(default=None, blank=True, to='sce.SubjectCategory', null=True),
        ),
        migrations.AddField(
            model_name='subject',
            name='department',
            field=models.ForeignKey(blank=True, to='sce.Department', null=True),
        ),
        migrations.AddField(
            model_name='subject',
            name='educative_program',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='alumni.EducativeProgram', null=True),
        ),
        migrations.AddField(
            model_name='subject',
            name='grade_level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Grade level', blank=True, to='alumni.GradeLevel', null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='marking_periods',
            field=models.ManyToManyField(related_name='course_set', blank=True, related_query_name='course', to='sce.MarkingPeriod'),
        ),
        migrations.AddField(
            model_name='course',
            name='school_year',
            field=models.ForeignKey(to='sce.SchoolYear'),
        ),
        migrations.AddField(
            model_name='course',
            name='students',
            field=models.ManyToManyField(related_name='course_set', through='sce.CourseEnrollment', blank=True, related_query_name='course', to='alumni.Student'),
        ),
        migrations.AddField(
            model_name='course',
            name='subject',
            field=models.ForeignKey(related_name='courses', to='sce.Subject'),
        ),
        migrations.AddField(
            model_name='course',
            name='teacher',
            field=models.ForeignKey(blank=True, to='alumni.Teacher', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='courseenrollment',
            unique_together=set([('course', 'student')]),
        ),
    ]
