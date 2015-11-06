# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import localflavor.us.models
from django.conf import settings
import django.db.models.deletion
import alumni.models
import django.core.validators
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassYear',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('year', alumni.models.IntegerRangeField(help_text='e.g. 2015', unique=True)),
                ('name', models.CharField(max_length=255, help_text='e.g. Class of 2015', blank=True)),
            ],
            options={
                'verbose_name': 'Class Year',
            },
        ),
        migrations.CreateModel(
            name='Cohort',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='EducativeProgram',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.CharField(max_length=100, blank=True, unique=True)),
                ('marking_periods', models.IntegerField()),
                ('num_of_levels', models.IntegerField()),
                ('order', models.IntegerField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='GradeLevel',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('number', models.IntegerField(verbose_name='Grade number')),
                ('name', models.CharField(max_length=100, verbose_name='Grade name', blank=True)),
                ('slug', models.CharField(max_length=100, verbose_name='slug', blank=True)),
                ('order', models.IntegerField(null=True, blank=True)),
                ('educative_program', models.ForeignKey(to='alumni.EducativeProgram')),
            ],
            options={
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='Institute',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('facebook', models.CharField(max_length=200, null=True, blank=True)),
                ('twitter', models.CharField(max_length=200, null=True, blank=True)),
                ('instagram', models.CharField(max_length=200, null=True, blank=True)),
                ('youtube', models.CharField(max_length=200, null=True, blank=True)),
                ('phone', localflavor.us.models.PhoneNumberField(max_length=20, null=True, blank=True)),
                ('email', models.EmailField(max_length=254, null=True, blank=True)),
                ('address', models.CharField(max_length=200, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='SchoolYear',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
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
            name='Student',
            fields=[
                ('account_ptr', models.OneToOneField(parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, auto_created=True)),
                ('enrollment', models.CharField(max_length=8, null=True, blank=True)),
                ('sex', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1, null=True, blank=True)),
                ('birthday', models.DateField(verbose_name='Birth Date', null=True, validators=[django.core.validators.MinValueValidator(datetime.date(1970, 1, 1))], blank=True)),
                ('phone', localflavor.us.models.PhoneNumberField(max_length=20, null=True, blank=True)),
                ('parent_email', models.EmailField(max_length=254, null=True, blank=True)),
                ('parent_phone', localflavor.us.models.PhoneNumberField(max_length=20, null=True, blank=True)),
                ('class_year', models.ForeignKey(verbose_name='Class year / School Generation', null=True, to='alumni.ClassYear', blank=True)),
                ('first_school_year', models.ForeignKey(to='alumni.SchoolYear', null=True, on_delete=django.db.models.deletion.SET_NULL)),
                ('grade_level', models.ForeignKey(to='alumni.GradeLevel', null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True)),
                ('institute', models.ForeignKey(to='alumni.Institute')),
            ],
            options={
                'ordering': ('last_name', 'first_name'),
            },
            bases=('authentication.account',),
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('account_ptr', models.OneToOneField(parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, auto_created=True)),
                ('phone', localflavor.us.models.PhoneNumberField(max_length=20)),
            ],
            options={
                'abstract': False,
            },
            bases=('authentication.account',),
        ),
        migrations.AddField(
            model_name='educativeprogram',
            name='institute',
            field=models.ForeignKey(to='alumni.Institute'),
        ),
        migrations.AddField(
            model_name='cohort',
            name='students',
            field=models.ManyToManyField(to='alumni.Student', related_query_name='cohort', related_name='cohorts', blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='gradelevel',
            unique_together=set([('number', 'educative_program')]),
        ),
    ]
