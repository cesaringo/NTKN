# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import sce.models
from django.conf import settings
import django.core.validators
import datetime
import localflavor.us.models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassYear',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('year', sce.models.IntegerRangeField(unique=True, help_text='e.g. 2015')),
                ('name', models.CharField(blank=True, max_length=255, help_text='e.g. Class of 2015')),
            ],
            options={
                'verbose_name': 'Class Year',
            },
        ),
        migrations.CreateModel(
            name='Cohort',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('cohort', models.ForeignKey(blank=True, to='sce.Cohort', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CourseEnrollment',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('course', models.ForeignKey(to='sce.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Department Name')),
            ],
        ),
        migrations.CreateModel(
            name='EducativeProgram',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(unique=True, max_length=100)),
                ('slug', models.CharField(unique=True, blank=True, max_length=100)),
                ('order', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='GradeLevel',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('number', models.IntegerField(verbose_name='Grade number')),
                ('name', models.CharField(blank=True, max_length=100, verbose_name='Grade name')),
                ('order', models.IntegerField(blank=True, null=True)),
                ('slug', models.CharField(blank=True, max_length=100, verbose_name='slug')),
                ('educative_program', models.ForeignKey(to='sce.EducativeProgram')),
            ],
            options={
                'ordering': ('number',),
            },
        ),
        migrations.CreateModel(
            name='MarkingPeriod',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(unique=True, max_length=255)),
                ('shortname', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('grades_due', models.DateField(validators=[django.core.validators.MinValueValidator(datetime.date(1970, 1, 1))], blank=True, null=True, help_text='If filled out, teachers will be notified when grades are due.')),
                ('active', models.BooleanField(default=False, help_text='Teachers may only enter grades for active marking periods. There may be more than one active marking period.')),
            ],
            options={
                'ordering': ('-start_date',),
            },
        ),
        migrations.CreateModel(
            name='SchoolYear',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
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
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('score', models.DecimalField(decimal_places=2, max_digits=4)),
                ('course_enrollment', models.ForeignKey(related_name='scores', to='sce.CourseEnrollment', related_query_name='score')),
                ('marking_period', models.ForeignKey(blank=True, to='sce.MarkingPeriod', on_delete=django.db.models.deletion.SET_NULL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('account_ptr', models.OneToOneField(serialize=False, auto_created=True, to=settings.AUTH_USER_MODEL, primary_key=True, parent_link=True)),
                ('mname', models.CharField(blank=True, max_length=100, null=True, verbose_name='Middle name')),
                ('sex', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=1, null=True)),
                ('bday', models.DateField(validators=[django.core.validators.MinValueValidator(datetime.date(1970, 1, 1))], blank=True, null=True, verbose_name='Birth Date')),
                ('enrollment', models.CharField(blank=True, max_length=8, null=True)),
                ('phone', localflavor.us.models.PhoneNumberField(blank=True, max_length=20, null=True)),
                ('parent_email', models.EmailField(blank=True, max_length=254)),
                ('parent_phone', localflavor.us.models.PhoneNumberField(blank=True, max_length=20, null=True)),
                ('class_year', models.ForeignKey(blank=True, to='sce.ClassYear', verbose_name='Class year / School Generation', null=True)),
                ('educative_program', models.ForeignKey(blank=True, to='sce.EducativeProgram', on_delete=django.db.models.deletion.SET_NULL, null=True)),
                ('first_school_year', models.ForeignKey(to='sce.SchoolYear', on_delete=django.db.models.deletion.SET_NULL, null=True)),
                ('year', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.SET_NULL, verbose_name='Grade level', to='sce.GradeLevel', null=True)),
            ],
            options={
                'permissions': (('view_student', 'View student'), ('view_contact_info', 'View contact info')),
                'ordering': ('last_name', 'first_name'),
            },
            bases=('authentication.account',),
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('fullname', models.CharField(max_length=255, verbose_name='Subject Name')),
                ('shortname', models.CharField(max_length=255, verbose_name='Key')),
                ('graded', models.BooleanField(default=True, help_text='Teachers can submit grades for this course')),
                ('description', models.TextField(blank=True, null=True)),
                ('level', models.IntegerField(null=True)),
                ('periods', models.CommaSeparatedIntegerField(blank=True, max_length=100)),
                ('order', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubjectCategory',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('order', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('account_ptr', models.OneToOneField(serialize=False, auto_created=True, to=settings.AUTH_USER_MODEL, primary_key=True, parent_link=True)),
                ('phone', localflavor.us.models.PhoneNumberField(max_length=20)),
            ],
            options={
                'abstract': False,
            },
            bases=('authentication.account',),
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
            field=models.ForeignKey(blank=True, to='sce.EducativeProgram', on_delete=django.db.models.deletion.SET_NULL, null=True),
        ),
        migrations.AddField(
            model_name='subject',
            name='grade_level',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.SET_NULL, verbose_name='Grade level', to='sce.GradeLevel', null=True),
        ),
        migrations.AddField(
            model_name='courseenrollment',
            name='student',
            field=models.ForeignKey(to='sce.Student'),
        ),
        migrations.AddField(
            model_name='course',
            name='marking_periods',
            field=models.ManyToManyField(to='sce.MarkingPeriod', blank=True, related_query_name='course', related_name='course_set'),
        ),
        migrations.AddField(
            model_name='course',
            name='school_year',
            field=models.ForeignKey(to='sce.SchoolYear'),
        ),
        migrations.AddField(
            model_name='course',
            name='students',
            field=models.ManyToManyField(through='sce.CourseEnrollment', to='sce.Student', blank=True, related_query_name='course', related_name='course_set'),
        ),
        migrations.AddField(
            model_name='course',
            name='subject',
            field=models.ForeignKey(to='sce.Subject', related_name='courses'),
        ),
        migrations.AddField(
            model_name='course',
            name='teacher',
            field=models.ForeignKey(blank=True, to='sce.Teacher', null=True),
        ),
        migrations.AddField(
            model_name='cohort',
            name='students',
            field=models.ManyToManyField(to='sce.Student', blank=True, related_query_name='cohort', related_name='cohort_set'),
        ),
        migrations.AlterUniqueTogether(
            name='gradelevel',
            unique_together=set([('number', 'educative_program')]),
        ),
        migrations.AlterUniqueTogether(
            name='courseenrollment',
            unique_together=set([('course', 'student')]),
        ),
    ]
