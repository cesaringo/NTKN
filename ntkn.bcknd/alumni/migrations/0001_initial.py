# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import datetime
import alumni.models
import localflavor.us.models
import django.core.validators
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassYear',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('year', alumni.models.IntegerRangeField(help_text='e.g. 2015', unique=True)),
                ('name', models.CharField(help_text='e.g. Class of 2015', max_length=255, blank=True)),
            ],
            options={
                'verbose_name': 'Class Year',
            },
        ),
        migrations.CreateModel(
            name='Cohort',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='EducativeProgram',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(unique=True, max_length=100)),
                ('slug', models.CharField(unique=True, max_length=100, blank=True)),
                ('num_marking_periods', models.IntegerField()),
                ('num_of_levels', models.IntegerField()),
                ('order', models.IntegerField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='GradeLevel',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
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
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('facebook', models.CharField(null=True, max_length=200, blank=True)),
                ('twitter', models.CharField(null=True, max_length=200, blank=True)),
                ('instagram', models.CharField(null=True, max_length=200, blank=True)),
                ('youtube', models.CharField(null=True, max_length=200, blank=True)),
                ('phone', localflavor.us.models.PhoneNumberField(null=True, max_length=20, blank=True)),
                ('email', models.EmailField(null=True, max_length=254, blank=True)),
                ('address', models.CharField(null=True, max_length=200, blank=True)),
            ],
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
            name='Student',
            fields=[
                ('account_ptr', models.OneToOneField(to=settings.AUTH_USER_MODEL, auto_created=True, primary_key=True, serialize=False, parent_link=True)),
                ('enrollment', models.CharField(null=True, max_length=8, blank=True)),
                ('sex', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], null=True, max_length=1, blank=True)),
                ('birthday', models.DateField(null=True, validators=[django.core.validators.MinValueValidator(datetime.date(1970, 1, 1))], verbose_name='Birth Date', blank=True)),
                ('phone', localflavor.us.models.PhoneNumberField(null=True, max_length=20, blank=True)),
                ('parent_email', models.EmailField(null=True, max_length=254, blank=True)),
                ('parent_phone', localflavor.us.models.PhoneNumberField(null=True, max_length=20, blank=True)),
                ('class_year', models.ForeignKey(to='alumni.ClassYear', verbose_name='Class year / School Generation', null=True, blank=True)),
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
                ('account_ptr', models.OneToOneField(to=settings.AUTH_USER_MODEL, auto_created=True, primary_key=True, serialize=False, parent_link=True)),
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
            field=models.ManyToManyField(related_name='cohorts', related_query_name='cohort', to='alumni.Student', blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='gradelevel',
            unique_together=set([('number', 'educative_program')]),
        ),
    ]
