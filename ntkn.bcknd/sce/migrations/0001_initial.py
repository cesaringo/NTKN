# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import datetime
from django.conf import settings
import localflavor.us.models
import sce.models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassYear',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('cohort', models.ForeignKey(null=True, blank=True, to='sce.Cohort')),
            ],
        ),
        migrations.CreateModel(
            name='CourseEnrollment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('is_active', models.BooleanField(default=True)),
                ('course', models.ForeignKey(to='sce.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(unique=True, verbose_name='Department Name', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='EducativeProgram',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('slug', models.CharField(unique=True, max_length=100, blank=True)),
                ('order', models.IntegerField(null=True, blank=True)),
                ('marking_periods', models.IntegerField()),
                ('num_of_levels', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='GradeLevel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('number', models.IntegerField(verbose_name='Grade number')),
                ('name', models.CharField(verbose_name='Grade name', max_length=100, blank=True)),
                ('order', models.IntegerField(null=True, blank=True)),
                ('slug', models.CharField(verbose_name='slug', max_length=100, blank=True)),
                ('educative_program', models.ForeignKey(to='sce.EducativeProgram')),
            ],
            options={
                'ordering': ('number',),
            },
        ),
        migrations.CreateModel(
            name='MarkingPeriod',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('shortname', models.CharField(max_length=255)),
                ('description', models.TextField(null=True, blank=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('grades_due', models.DateField(null=True, validators=[django.core.validators.MinValueValidator(datetime.date(1970, 1, 1))], help_text='If filled out, teachers will be notified when grades are due.', blank=True)),
                ('active', models.BooleanField(help_text='Teachers may only enter grades for active marking periods. There may be more than one active marking period.', default=False)),
            ],
            options={
                'ordering': ('shortname',),
            },
        ),
        migrations.CreateModel(
            name='SchoolYear',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('score', models.DecimalField(null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(10.0)], max_digits=3, decimal_places=1, blank=True)),
                ('course_enrollment', models.ForeignKey(related_query_name='score', related_name='scores', to='sce.CourseEnrollment')),
                ('marking_period', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='sce.MarkingPeriod')),
            ],
            options={
                'ordering': ('marking_period',),
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('account_ptr', models.OneToOneField(auto_created=True, to=settings.AUTH_USER_MODEL, serialize=False, primary_key=True, parent_link=True)),
                ('mname', models.CharField(verbose_name='Middle name', max_length=100, null=True, blank=True)),
                ('sex', models.CharField(max_length=1, null=True, choices=[('M', 'Male'), ('F', 'Female')], blank=True)),
                ('bday', models.DateField(verbose_name='Birth Date', validators=[django.core.validators.MinValueValidator(datetime.date(1970, 1, 1))], null=True, blank=True)),
                ('enrollment', models.CharField(max_length=8, null=True, blank=True)),
                ('phone', localflavor.us.models.PhoneNumberField(max_length=20, null=True, blank=True)),
                ('parent_email', models.EmailField(max_length=254, blank=True)),
                ('parent_phone', localflavor.us.models.PhoneNumberField(max_length=20, null=True, blank=True)),
                ('class_year', models.ForeignKey(null=True, verbose_name='Class year / School Generation', blank=True, to='sce.ClassYear')),
                ('educative_program', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='sce.EducativeProgram')),
                ('first_school_year', models.ForeignKey(null=True, to='sce.SchoolYear', on_delete=django.db.models.deletion.SET_NULL)),
                ('year', models.ForeignKey(null=True, verbose_name='Grade level', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='sce.GradeLevel')),
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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('is_active', models.BooleanField(default=True)),
                ('fullname', models.CharField(verbose_name='Subject Name', max_length=255)),
                ('shortname', models.CharField(verbose_name='Key', max_length=255)),
                ('graded', models.BooleanField(help_text='Teachers can submit grades for this course', default=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('level', models.IntegerField(null=True)),
                ('periods', models.CommaSeparatedIntegerField(max_length=100, blank=True)),
                ('order', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubjectCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=150)),
                ('order', models.IntegerField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('account_ptr', models.OneToOneField(auto_created=True, to=settings.AUTH_USER_MODEL, serialize=False, primary_key=True, parent_link=True)),
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
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='sce.EducativeProgram'),
        ),
        migrations.AddField(
            model_name='subject',
            name='grade_level',
            field=models.ForeignKey(null=True, verbose_name='Grade level', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='sce.GradeLevel'),
        ),
        migrations.AddField(
            model_name='courseenrollment',
            name='student',
            field=models.ForeignKey(to='sce.Student'),
        ),
        migrations.AddField(
            model_name='course',
            name='marking_periods',
            field=models.ManyToManyField(related_query_name='course', related_name='course_set', to='sce.MarkingPeriod', blank=True),
        ),
        migrations.AddField(
            model_name='course',
            name='school_year',
            field=models.ForeignKey(to='sce.SchoolYear'),
        ),
        migrations.AddField(
            model_name='course',
            name='students',
            field=models.ManyToManyField(related_query_name='course', through='sce.CourseEnrollment', related_name='course_set', to='sce.Student', blank=True),
        ),
        migrations.AddField(
            model_name='course',
            name='subject',
            field=models.ForeignKey(related_name='courses', to='sce.Subject'),
        ),
        migrations.AddField(
            model_name='course',
            name='teacher',
            field=models.ForeignKey(null=True, blank=True, to='sce.Teacher'),
        ),
        migrations.AddField(
            model_name='cohort',
            name='students',
            field=models.ManyToManyField(related_query_name='cohort', related_name='cohorts', to='sce.Student', blank=True),
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
