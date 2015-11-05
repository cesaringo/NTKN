# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings
import django.core.validators
import django.db.models.deletion
import localflavor.us.models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_auto_20151104_1609'),
        ('students', '0003_auto_20151104_1509'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cohort',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('students', models.ManyToManyField(related_name='cohorts', related_query_name='cohort', to='students.Student', blank=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('cohort', models.ForeignKey(to='sce.Cohort', null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='CourseEnrollment',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True)),
                ('course', models.ForeignKey(to='sce.Course')),
                ('student', models.ForeignKey(to='students.Student')),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='Department Name', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='MarkingPeriod',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('shortname', models.CharField(max_length=255)),
                ('description', models.TextField(null=True, blank=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('grades_due', models.DateField(validators=[django.core.validators.MinValueValidator(datetime.date(1970, 1, 1))], help_text='If filled out, teachers will be notified when grades are due.', null=True, blank=True)),
                ('active', models.BooleanField(help_text='Teachers may only enter grades for active marking periods. There may be more than one active marking period.', default=False)),
            ],
            options={
                'ordering': ('shortname',),
            },
        ),
        migrations.CreateModel(
            name='SchoolYear',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('score', models.DecimalField(validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(10.0)], decimal_places=1, max_digits=3, null=True, blank=True)),
                ('course_enrollment', models.ForeignKey(related_name='scores', related_query_name='score', to='sce.CourseEnrollment')),
                ('marking_period', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='sce.MarkingPeriod', null=True, blank=True)),
            ],
            options={
                'ordering': ('marking_period',),
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150)),
                ('order', models.IntegerField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('account_ptr', models.OneToOneField(serialize=False, auto_created=True, parent_link=True, to=settings.AUTH_USER_MODEL, primary_key=True)),
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
            field=models.ForeignKey(to='sce.SubjectCategory', default=None, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='subject',
            name='department',
            field=models.ForeignKey(to='sce.Department', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='subject',
            name='educative_program',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='students.EducativeProgram', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='subject',
            name='grade_level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Grade level', to='students.GradeLevel', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='course',
            name='marking_periods',
            field=models.ManyToManyField(related_name='course_set', related_query_name='course', to='sce.MarkingPeriod', blank=True),
        ),
        migrations.AddField(
            model_name='course',
            name='school_year',
            field=models.ForeignKey(to='sce.SchoolYear'),
        ),
        migrations.AddField(
            model_name='course',
            name='students',
            field=models.ManyToManyField(related_name='course_set', through='sce.CourseEnrollment', related_query_name='course', to='students.Student', blank=True),
        ),
        migrations.AddField(
            model_name='course',
            name='subject',
            field=models.ForeignKey(related_name='courses', to='sce.Subject'),
        ),
        migrations.AddField(
            model_name='course',
            name='teacher',
            field=models.ForeignKey(to='sce.Teacher', null=True, blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='courseenrollment',
            unique_together=set([('course', 'student')]),
        ),
    ]
