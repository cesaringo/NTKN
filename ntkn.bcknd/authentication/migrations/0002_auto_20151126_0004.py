# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import Group
from django.db import models, migrations
from authentication.models import Account


def load_initial_data(apps, schema_editor):
    print('\nLoading initial data authentication module')
    print('\n-Loading Groups')
    groups = ['student', 'teacher', 'director', 'administrator']
    for item in groups:
        group = Group(name=item)
        group.save()
        print('--added Group: ' + group.__str__())

    print('\nLoading Administrators')
    admin1 = Account.objects.create_superuser(username='cesaringo', email='cesr90@gmail.com',
                                              password='12345')
    print('--added Administrator: ' + admin1.__str__())
    admin2 = Account.objects.create_superuser(username='damaris', email='gdamaris.6@gmail.com',
                                              password='12345')
    print('--added Administrator: ' + admin2.__str__())


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_initial_data),
    ]
