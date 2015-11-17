# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import django.db.models.deletion
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('alumni', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('cohort', models.ForeignKey(to='alumni.Cohort')),
            ],
        ),
        migrations.CreateModel(
            name='CourseEnrollment',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('is_active', models.BooleanField(default=True)),
                ('course', models.ForeignKey(to='sce.Course')),
                ('student', models.ForeignKey(to='alumni.Student')),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Department Name', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='MarkingPeriod',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('shortname', models.CharField(max_length=255)),
                ('description', models.TextField(null=True, blank=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('grades_due', models.DateField(null=True, help_text='If filled out, teachers will be notified when grades are due.', blank=True, validators=[django.core.validators.MinValueValidator(datetime.date(1970, 1, 1))])),
                ('active', models.BooleanField(help_text='Teachers may only enter grades for active marking periods. There may be more than one active marking period.', default=False)),
                ('educative_program', models.ForeignKey(to='alumni.EducativeProgram')),
            ],
            options={
                'ordering': ('shortname',),
            },
        ),
        migrations.CreateModel(
            name='SchoolYear',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100, unique=True)),
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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('score', models.DecimalField(null=True, max_digits=3, blank=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(10.0)], decimal_places=1)),
                ('course_enrollment', models.ForeignKey(to='sce.CourseEnrollment', related_name='scores', related_query_name='score')),
                ('marking_period', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.SET_NULL, null=True, to='sce.MarkingPeriod')),
            ],
            options={
                'ordering': ('marking_period',),
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('is_active', models.BooleanField(default=True)),
                ('fullname', models.CharField(max_length=255, verbose_name='Subject Name')),
                ('shortname', models.CharField(max_length=255, verbose_name='Key')),
                ('graded', models.BooleanField(help_text='Teachers can submit grades for this course', default=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('level', models.IntegerField(null=True)),
                ('order', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubjectCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=150)),
                ('order', models.IntegerField(null=True, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='subject',
            name='category',
            field=models.ForeignKey(default=None, blank=True, to='sce.SubjectCategory', null=True),
        ),
        migrations.AddField(
            model_name='subject',
            name='cohorts',
            field=models.ManyToManyField(to='alumni.Cohort'),
        ),
        migrations.AddField(
            model_name='subject',
            name='department',
            field=models.ForeignKey(blank=True, to='sce.Department', null=True),
        ),
        migrations.AddField(
            model_name='subject',
            name='educative_program',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.SET_NULL, null=True, to='alumni.EducativeProgram'),
        ),
        migrations.AddField(
            model_name='subject',
            name='grade_level',
            field=models.ForeignKey(verbose_name='Grade level', blank=True, on_delete=django.db.models.deletion.SET_NULL, null=True, to='alumni.GradeLevel'),
        ),
        migrations.AddField(
            model_name='course',
            name='marking_periods',
            field=models.ManyToManyField(related_name='course_set', to='sce.MarkingPeriod', blank=True, related_query_name='course'),
        ),
        migrations.AddField(
            model_name='course',
            name='school_year',
            field=models.ForeignKey(to='sce.SchoolYear'),
        ),
        migrations.AddField(
            model_name='course',
            name='students',
            field=models.ManyToManyField(related_name='course_set', through='sce.CourseEnrollment', to='alumni.Student', blank=True, related_query_name='course'),
        ),
        migrations.AddField(
            model_name='course',
            name='subject',
            field=models.ForeignKey(to='sce.Subject', related_name='courses'),
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
