# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import alumni.models
import django.db.models.deletion
import localflavor.us.models
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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('year', alumni.models.IntegerRangeField(unique=True, help_text='e.g. 2015')),
                ('name', models.CharField(help_text='e.g. Class of 2015', blank=True, max_length=255)),
            ],
            options={
                'verbose_name': 'Class Year',
            },
        ),
        migrations.CreateModel(
            name='Cohort',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='EducativeProgram',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('slug', models.CharField(unique=True, blank=True, max_length=100)),
                ('num_marking_periods', models.IntegerField()),
                ('num_of_levels', models.IntegerField()),
                ('order', models.IntegerField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='GradeLevel',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('number', models.IntegerField(verbose_name='Grade number')),
                ('name', models.CharField(blank=True, verbose_name='Grade name', max_length=100)),
                ('slug', models.CharField(blank=True, verbose_name='slug', max_length=100)),
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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('facebook', models.CharField(null=True, blank=True, max_length=200)),
                ('twitter', models.CharField(null=True, blank=True, max_length=200)),
                ('instagram', models.CharField(null=True, blank=True, max_length=200)),
                ('youtube', models.CharField(null=True, blank=True, max_length=200)),
                ('phone', localflavor.us.models.PhoneNumberField(null=True, blank=True, max_length=20)),
                ('email', models.EmailField(null=True, blank=True, max_length=254)),
                ('address', models.CharField(null=True, blank=True, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='SchoolYear',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
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
                ('account_ptr', models.OneToOneField(to=settings.AUTH_USER_MODEL, parent_link=True, serialize=False, primary_key=True, auto_created=True)),
                ('enrollment', models.CharField(null=True, blank=True, max_length=8)),
                ('sex', models.CharField(blank=True, null=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('birthday', models.DateField(null=True, blank=True, verbose_name='Birth Date', validators=[django.core.validators.MinValueValidator(datetime.date(1970, 1, 1))])),
                ('phone', localflavor.us.models.PhoneNumberField(null=True, blank=True, max_length=20)),
                ('parent_email', models.EmailField(null=True, blank=True, max_length=254)),
                ('parent_phone', localflavor.us.models.PhoneNumberField(null=True, blank=True, max_length=20)),
                ('class_year', models.ForeignKey(to='alumni.ClassYear', null=True, blank=True, verbose_name='Class year / School Generation')),
                ('first_school_year', models.ForeignKey(to='alumni.SchoolYear', null=True, on_delete=django.db.models.deletion.SET_NULL)),
                ('grade_level', models.ForeignKey(to='alumni.GradeLevel', null=True, blank=True, on_delete=django.db.models.deletion.SET_NULL)),
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
                ('account_ptr', models.OneToOneField(to=settings.AUTH_USER_MODEL, parent_link=True, serialize=False, primary_key=True, auto_created=True)),
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
            field=models.ManyToManyField(to='alumni.Student', blank=True, related_name='cohorts', related_query_name='cohort'),
        ),
        migrations.AlterUniqueTogether(
            name='gradelevel',
            unique_together=set([('number', 'educative_program')]),
        ),
    ]
