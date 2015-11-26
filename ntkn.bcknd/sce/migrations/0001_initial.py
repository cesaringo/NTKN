# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings
import django.core.validators
import sce.models
import localflavor.us.models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassYear',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', sce.models.IntegerRangeField(unique=True, help_text='e.g. 2015')),
                ('name', models.CharField(blank=True, help_text='e.g. Class of 2015', max_length=255)),
            ],
            options={
                'verbose_name': 'Class Year',
            },
        ),
        migrations.CreateModel(
            name='Cohort',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(null=True, max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('cohort', models.ForeignKey(to='sce.Cohort')),
            ],
        ),
        migrations.CreateModel(
            name='CourseEnrollment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('course', models.ForeignKey(to='sce.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(unique=True, verbose_name='Department Name', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='EducativeProgram',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(unique=True, max_length=100)),
                ('slug', models.CharField(blank=True, unique=True, max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('order', models.IntegerField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='GradeLevel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(verbose_name='Grade number')),
                ('name', models.CharField(blank=True, verbose_name='Grade name', max_length=100)),
                ('slug', models.CharField(blank=True, verbose_name='slug', max_length=100)),
                ('order', models.IntegerField(null=True, blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('educative_program', models.ForeignKey(to='sce.EducativeProgram')),
            ],
            options={
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='Institute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('facebook', models.CharField(null=True, blank=True, max_length=200)),
                ('twitter', models.CharField(null=True, blank=True, max_length=200)),
                ('instagram', models.CharField(null=True, blank=True, max_length=200)),
                ('youtube', models.CharField(null=True, blank=True, max_length=200)),
                ('phone', localflavor.us.models.PhoneNumberField(null=True, blank=True, max_length=20)),
                ('email', models.EmailField(null=True, blank=True, max_length=254)),
                ('address', models.CharField(null=True, blank=True, max_length=200)),
                ('order', models.IntegerField(null=True, blank=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='MarkingPeriod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('shortname', models.CharField(max_length=255)),
                ('description', models.TextField(null=True, blank=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('grades_due', models.DateField(null=True, validators=[django.core.validators.MinValueValidator(datetime.date(1970, 1, 1))], help_text='If filled out, teachers will be notified when grades are due.', blank=True)),
                ('is_active', models.BooleanField(default=False, help_text='Teachers may only enter grades for active marking periods. There may be more than one active marking period.')),
                ('educative_program', models.ForeignKey(to='sce.EducativeProgram')),
            ],
            options={
                'ordering': ('shortname',),
            },
        ),
        migrations.CreateModel(
            name='SchoolYear',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(validators=[django.core.validators.MinValueValidator(datetime.date(1970, 1, 1))])),
                ('end_date', models.DateField(validators=[django.core.validators.MinValueValidator(datetime.date(1970, 1, 1))])),
                ('is_active', models.BooleanField(default=False)),
                ('slug', models.CharField(blank=True, unique=True, max_length=100)),
                ('educative_program', models.ForeignKey(to='sce.EducativeProgram')),
            ],
            options={
                'ordering': ('start_date',),
            },
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.DecimalField(decimal_places=1, max_digits=3, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(10.0)], blank=True)),
                ('course_enrollment', models.ForeignKey(related_name='scores', related_query_name='score', to='sce.CourseEnrollment')),
                ('marking_period', models.ForeignKey(null=True, blank=True, to='sce.MarkingPeriod', on_delete=django.db.models.deletion.SET_NULL)),
            ],
            options={
                'ordering': ('marking_period',),
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('account_ptr', models.OneToOneField(auto_created=True, parent_link=True, primary_key=True, to=settings.AUTH_USER_MODEL, serialize=False)),
                ('enrollment', models.CharField(null=True, blank=True, max_length=8)),
                ('sex', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], null=True, blank=True, max_length=1)),
                ('birthday', models.DateField(null=True, validators=[django.core.validators.MinValueValidator(datetime.date(1970, 1, 1))], verbose_name='Birth Date', blank=True)),
                ('phone', localflavor.us.models.PhoneNumberField(null=True, blank=True, max_length=20)),
                ('parent_email', models.EmailField(null=True, blank=True, max_length=254)),
                ('parent_phone', localflavor.us.models.PhoneNumberField(null=True, blank=True, max_length=20)),
                ('class_year', models.ForeignKey(null=True, blank=True, to='sce.ClassYear', verbose_name='Class year / School Generation')),
                ('grade_level', models.ForeignKey(null=True, blank=True, to='sce.GradeLevel', on_delete=django.db.models.deletion.SET_NULL)),
                ('institute', models.ForeignKey(to='sce.Institute')),
            ],
            options={
                'ordering': ('last_name', 'first_name'),
            },
            bases=('authentication.account',),
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('name', models.CharField(verbose_name='Subject Name', max_length=255)),
                ('code', models.CharField(verbose_name='Key', max_length=255)),
                ('graded', models.BooleanField(default=True, help_text='Teachers can submit grades for this course')),
                ('description', models.TextField(null=True, blank=True)),
                ('level', models.IntegerField(null=True)),
                ('order', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubjectCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('order', models.IntegerField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('account_ptr', models.OneToOneField(auto_created=True, parent_link=True, primary_key=True, to=settings.AUTH_USER_MODEL, serialize=False)),
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
            field=models.ForeignKey(null=True, blank=True, to='sce.SubjectCategory', default=None),
        ),
        migrations.AddField(
            model_name='subject',
            name='department',
            field=models.ForeignKey(null=True, blank=True, to='sce.Department'),
        ),
        migrations.AddField(
            model_name='subject',
            name='grade_level',
            field=models.ForeignKey(null=True, blank=True, to='sce.GradeLevel', verbose_name='Grade level', on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='educativeprogram',
            name='institute',
            field=models.ForeignKey(to='sce.Institute'),
        ),
        migrations.AddField(
            model_name='courseenrollment',
            name='student',
            field=models.ForeignKey(to='sce.Student'),
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
            field=models.ManyToManyField(related_name='course_set', to='sce.Student', blank=True, related_query_name='course', through='sce.CourseEnrollment'),
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
            name='grade_levels',
            field=models.ManyToManyField(related_name='cohorts', to='sce.GradeLevel', blank=True, related_query_name='cohort'),
        ),
        migrations.AddField(
            model_name='cohort',
            name='students',
            field=models.ManyToManyField(related_name='cohorts', to='sce.Student', blank=True, related_query_name='cohort'),
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
