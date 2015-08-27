# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import localflavor.us.models
import django.db.models.deletion
import sce.models
import django.core.validators
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassYear',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('year', sce.models.IntegerRangeField(unique=True, help_text='e.g. 2015')),
                ('name', models.CharField(max_length=255, help_text='e.g. Class of 2015', blank=True)),
            ],
            options={
                'verbose_name': 'Class Year',
            },
        ),
        migrations.CreateModel(
            name='Cohort',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('is_active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CourseEnrollment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('is_active', models.BooleanField(default=True)),
                ('course', models.ForeignKey(to='sce.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Department Name')),
            ],
        ),
        migrations.CreateModel(
            name='EducativeProgram',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('slug', models.CharField(unique=True, max_length=100, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='GradeLevel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('number', models.IntegerField(verbose_name='Grade number')),
                ('name', models.CharField(unique=True, max_length=150, verbose_name='Grade name')),
            ],
            options={
                'ordering': ('number',),
            },
        ),
        migrations.CreateModel(
            name='MarkingPeriod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('shortname', models.CharField(max_length=255)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('grades_due', models.DateField(validators=[django.core.validators.MinValueValidator(datetime.date(1970, 1, 1))], blank=True, help_text='If filled out, teachers will be notified when grades are due.', null=True)),
                ('active', models.BooleanField(default=False, help_text='Teachers may only enter grades for active marking periods. There may be more than one active marking period.')),
            ],
            options={
                'ordering': ('-start_date',),
            },
        ),
        migrations.CreateModel(
            name='SchoolYear',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
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
            name='Student',
            fields=[
                ('account_ptr', models.OneToOneField(to=settings.AUTH_USER_MODEL, serialize=False, primary_key=True, auto_created=True, parent_link=True)),
                ('mname', models.CharField(max_length=100, verbose_name='Middle name', blank=True, null=True)),
                ('sex', models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')], blank=True, null=True)),
                ('bday', models.DateField(validators=[django.core.validators.MinValueValidator(datetime.date(1970, 1, 1))], blank=True, verbose_name='Birth Date', null=True)),
                ('enrollment', models.CharField(max_length=8, blank=True, null=True)),
                ('phone', localflavor.us.models.PhoneNumberField(max_length=20, blank=True, null=True)),
                ('parent_email', models.EmailField(max_length=254, editable=False, blank=True)),
                ('parent_phone', localflavor.us.models.PhoneNumberField(max_length=20, blank=True, null=True)),
                ('class_year', models.ForeignKey(verbose_name='Class year / School Generation', to='sce.ClassYear', blank=True, null=True)),
                ('cohorts', models.ManyToManyField(blank=True, to='sce.Cohort')),
                ('educative_program', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='sce.EducativeProgram', blank=True, null=True)),
                ('first_school_year', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='sce.SchoolYear', null=True)),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Grade level', to='sce.GradeLevel', blank=True, null=True)),
            ],
            options={
                'ordering': ('last_name', 'first_name'),
                'permissions': (('view_student', 'View student'), ('view_contact_info', 'View contact info')),
            },
            bases=('authentication.account',),
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('is_active', models.BooleanField(default=True)),
                ('fullname', models.CharField(unique=True, max_length=255, verbose_name='Full Course Name')),
                ('shortname', models.CharField(max_length=255, verbose_name='Short Name')),
                ('graded', models.BooleanField(default=True, help_text='Teachers can submit grades for this course')),
                ('description', models.TextField(blank=True, null=True)),
                ('periods', models.CommaSeparatedIntegerField(max_length=100, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubjectCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=150)),
                ('order', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('account_ptr', models.OneToOneField(to=settings.AUTH_USER_MODEL, serialize=False, primary_key=True, auto_created=True, parent_link=True)),
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
            field=models.ForeignKey(to='sce.SubjectCategory', blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='subject',
            name='department',
            field=models.ForeignKey(to='sce.Department', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='subject',
            name='educative_program',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='sce.EducativeProgram', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='courseenrollment',
            name='student',
            field=models.ForeignKey(to='sce.Student'),
        ),
        migrations.AddField(
            model_name='course',
            name='marking_period',
            field=models.ManyToManyField(blank=True, to='sce.MarkingPeriod'),
        ),
        migrations.AddField(
            model_name='course',
            name='school_year',
            field=models.ForeignKey(to='sce.SchoolYear'),
        ),
        migrations.AddField(
            model_name='course',
            name='subject',
            field=models.ForeignKey(to='sce.Subject', related_name='courses'),
        ),
        migrations.AddField(
            model_name='course',
            name='teacher',
            field=models.ForeignKey(to='sce.Teacher', blank=True),
        ),
        migrations.AddField(
            model_name='cohort',
            name='students',
            field=models.ManyToManyField(blank=True, to='sce.Student'),
        ),
        migrations.AlterUniqueTogether(
            name='courseenrollment',
            unique_together=set([('course', 'student')]),
        ),
    ]
