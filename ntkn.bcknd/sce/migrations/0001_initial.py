# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import django.core.validators
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('alumni', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(null=True, max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('cohort', models.ForeignKey(null=True, blank=True, to='alumni.Cohort')),
            ],
        ),
        migrations.CreateModel(
            name='CourseEnrollment',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('is_active', models.BooleanField(default=True)),
                ('course', models.ForeignKey(to='sce.Course')),
                ('student', models.ForeignKey(to='alumni.Student')),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(unique=True, verbose_name='Department Name', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='MarkingPeriod',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('shortname', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('grades_due', models.DateField(help_text='If filled out, teachers will be notified when grades are due.', validators=[django.core.validators.MinValueValidator(datetime.date(1970, 1, 1))], null=True, blank=True)),
                ('active', models.BooleanField(help_text='Teachers may only enter grades for active marking periods. There may be more than one active marking period.', default=False)),
            ],
            options={
                'ordering': ('shortname',),
            },
        ),
        migrations.CreateModel(
            name='SchoolYear',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
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
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('score', models.DecimalField(validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(10.0)], decimal_places=1, null=True, blank=True, max_digits=3)),
                ('course_enrollment', models.ForeignKey(related_query_name='score', related_name='scores', to='sce.CourseEnrollment')),
                ('marking_period', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, null=True, blank=True, to='sce.MarkingPeriod')),
            ],
            options={
                'ordering': ('marking_period',),
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('is_active', models.BooleanField(default=True)),
                ('fullname', models.CharField(verbose_name='Subject Name', max_length=255)),
                ('shortname', models.CharField(verbose_name='Key', max_length=255)),
                ('graded', models.BooleanField(help_text='Teachers can submit grades for this course', default=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('level', models.IntegerField(null=True)),
                ('order', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubjectCategory',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=150)),
                ('order', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='subject',
            name='category',
            field=models.ForeignKey(null=True, default=None, blank=True, to='sce.SubjectCategory'),
        ),
        migrations.AddField(
            model_name='subject',
            name='department',
            field=models.ForeignKey(null=True, blank=True, to='sce.Department'),
        ),
        migrations.AddField(
            model_name='subject',
            name='educative_program',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, null=True, blank=True, to='alumni.EducativeProgram'),
        ),
        migrations.AddField(
            model_name='subject',
            name='grade_level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, null=True, verbose_name='Grade level', blank=True, to='alumni.GradeLevel'),
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
            field=models.ManyToManyField(through='sce.CourseEnrollment', related_name='course_set', blank=True, related_query_name='course', to='alumni.Student'),
        ),
        migrations.AddField(
            model_name='course',
            name='subject',
            field=models.ForeignKey(related_name='courses', to='sce.Subject'),
        ),
        migrations.AddField(
            model_name='course',
            name='teacher',
            field=models.ForeignKey(null=True, blank=True, to='alumni.Teacher'),
        ),
        migrations.AlterUniqueTogether(
            name='courseenrollment',
            unique_together=set([('course', 'student')]),
        ),
    ]
