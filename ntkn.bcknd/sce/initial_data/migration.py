# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models, migrations
from sce.models import (
    EducativeProgram, GradeLevel, Cohort, SubjectCategory, Subject)
import csv
from slugify import slugify
from students.models import Institute



def load_cohorts(apps, schema_editor):
    print('\nLoading Cohorts')
    grade_levels = GradeLevel.objects.all()
    basic_groups = ["A", "B", "C", "D"]

    for grade_level in grade_levels:
        print('-'+grade_level.__str__()+str(grade_level.order))
        name = "-"
        if grade_level.number == 1:
            name = "Primero "
        elif grade_level.number == 2:
            name = "Segundo "
        elif grade_level.number == 3:
            name = "Tercero "
        elif grade_level.number == 4:
            name = "Cuarto "
        elif grade_level.number == 5:
            name = "Quinto "
        elif grade_level.number== 6:
            name = "Sexto "
        for basic_group in basic_groups:
            cohort = Cohort(name = name+basic_group)
            cohort.save()
            print('--added '+ cohort.__str__())


def load_subjects(apps, schema_editor):
    print('\nLoading Subjects')
    categories = [
        'Lenguaje y comunicación',
        'Pensamiento matemático',
        'Exploración y compreensión del mundo natural y social',
        'Desarrollo personal y para la convivencia'
    ]
    id = 1
    for category in categories:
        subjectCategory = SubjectCategory(pk=id, id=id, name=category, order = id)
        subjectCategory.save()
        print ('-added category ' + subjectCategory.__str__())
        id += 1

    fields = []
    with open('sce/initial_data/subjects.csv',  'rt', encoding='utf8') as f:
        reader = csv.reader(f)
        for row in reader:
            if reader.line_num == 1:
                fields = row
            else:
                subject = Subject(
                    fullname=row[1],
                    #key='',
                    #is_active=True,
                    #description='',
                    educative_program=EducativeProgram.objects.get(pk=row[5]),
                    category=SubjectCategory.objects.get(pk=row[6]),
                    level = row[7],
                    grade_level = GradeLevel.objects.get(pk=row [8])

                )
                subject.save()
                print('--added subject '+ subject.__str__() + ' in category ' + subject.category.__str__())


class Migration(migrations.Migration):
    dependencies = [
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_institutes),
        migrations.RunPython(load_educative_programs),
        migrations.RunPython(load_grade_levels),

        #migrations.RunPython(load_cohorts),
        #migrations.RunPython(load_subjects)
    ]
