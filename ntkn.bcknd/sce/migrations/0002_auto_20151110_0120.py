# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.db import models, migrations
from sce.models import SubjectCategory, Subject, SchoolYear, MarkingPeriod
from alumni.models import GradeLevel, EducativeProgram
import csv

def load_initial_sce_data(apps, schema_editor):
    print('\nLoading initial data for sce module')

    # School Years
    school_year = SchoolYear(
        name='2015 - 2016',
        start_date=datetime.now(),
        end_date=datetime.now()
    )
    school_year.save()
    print('\n--added School Year: ' + school_year.__str__())

    # Subjects
    print('\n-loading Subjects')
    categories = [
        'Lenguaje y '
        'municación',
        'Pensamiento matemático',
        'Exploración y compreensión del mundo natural y social',
        'Desarrollo personal y para la convivencia'
    ]
    id = 1
    for category in categories:
        subject_category = SubjectCategory(pk=id, id=id, name=category, order = id)
        subject_category.save()
        print('--added SubjectCategory ' + subject_category.__str__())
        id += 1

    with open('sce/initial_data/subjects.csv', 'rt', encoding='utf8') as f:
        reader = csv.reader(f)
        for row in reader:
            if reader.line_num == 1:
                pass
            else:
                subject = Subject(
                    fullname=row[1],
                    #key='',
                    #is_active=True,
                    #description='',
                    educative_program=EducativeProgram.objects.get(pk=row[5]),
                    category=SubjectCategory.objects.get(pk=row[6]),
                    level=row[7],
                    grade_level=GradeLevel.objects.get(pk=row[8])

                )
                subject.save()
                print('--added subject '+ subject.__str__() + ' in category ' + subject.category.__str__())

    # Marking period
    educative_programs = EducativeProgram.objects.all()
    for educative_program in educative_programs:
        for partial in range(1, educative_program.num_marking_periods + 1):
            marking_period = MarkingPeriod(name='Parcial ' + str(partial) + ' ' + educative_program.name,
                                           shortname='P ' + str(partial), start_date=datetime.min,
                                           end_date=datetime.min,
                                           educative_program=educative_program)
            marking_period.save()
            print('--added Marking Period: ' + marking_period.__str__())



class Migration(migrations.Migration):
    dependencies = [
        ('sce', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_initial_sce_data),
    ]
