# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
from django.db import models, migrations
from sce.models import *
import csv
from slugify import slugify

def load_initial_data(apps, schema_editor):
    print('\n-Loading Institutes')
    institute = Institute(
        name='Colegio Natkan',
    )
    institute.save()
    print('--added Institute: ' + institute.__str__())


    print("\n-Loading educative programs")
    institute = Institute.objects.get(pk=1)
    with open('sce/initial_data/educative_programs.csv', 'rt', encoding='utf8') as f:
        reader = csv.reader(f)
        for row in reader:
            if reader.line_num == 1:
                pass
            else:
                educative_program = EducativeProgram(
                    name=row[0],
                    slug=slugify(row[0], to_lower=True),
                    order=row[2],
                    institute=institute
                )
                educative_program.save()
                print('--added EducativeProgram: ' + educative_program.__str__())
    return 0
    print("\n-Loading grade levels")
    with open('sce/initial_data/grade_levels.csv', 'rt', encoding='utf8') as f:
        reader = csv.reader(f)
        for row in reader:
            grade_level = GradeLevel(
                number=row[0],
                name=row[1],
                slug=slugify(row[1], to_lower=True),
                order=row[0],
                educative_program=EducativeProgram.get(slug=row[2])
            )
            grade_level.save()
            print('--added Grade level: ' + grade_level.__str__())


    print('\n-Loading Cohorts')
    basic_cohorts = ["A", "B", "C", "D", "E"]
    #englis_cohorts = ["Básico (G1)", "Básico (G2)", "Básico (G3)"]

    for basic_cohort in basic_cohorts:
        cohort = Cohort(name=basic_cohort)
        cohort.save()
        print('--added ' + cohort.__str__())
        for grade_level in GradeLevel.objects.all():
            grade_level.cohort_set.add(cohort)
            print('Added Cohort: {0} to gradelevel: {1}'.format(cohort.__str__()), grade_level.__str__())


    print('\n-Load sample alumni')
    grade_levels = GradeLevel.objects.all()
    with open('sce/initial_data/institute_students.csv', 'rt', encoding='utf8') as f:
        reader = csv.reader(f)
        for row in reader:
            if reader.line_num == 1:
                pass
            elif reader.line_num == 40:
                break
            else:
                if row[3] == 'kinder':
                    row[3] = 'preescolar'
                student = Student(
                    institute_id=1,
                    first_name=row[0],
                    last_name=row[1] + ' ' + row[2],
                    grade_level=grade_levels.get(educative_program__slug=row[3], number=row[5].replace('NULL', '')),
                    is_active=row[4]
                )
                student.save()
                print('--added Student: ' + student.__str__())

    print('\n-Load sample teachers')
    teacher1 = Teacher(first_name='José Enrique', last_name='Alvarez Estrada', is_active=True)
    teacher2 = Teacher(first_name='María Montserrat', last_name='Ramírez', is_active=True)
    teacher1.save()
    teacher1.set_password(teacher1.username)
    teacher1.save()
    teacher2.save()
    print('\n--added Teacher:' + teacher1.__str__())
    print('\n--added Teacher:' + teacher2.__str__())




    # School Years
    print('\nLoading SchoolYears')
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
        subject_category = SubjectCategory(pk=id, id=id, name=category, order=id)
        subject_category.save()
        print('--added SubjectCategory ' + subject_category.__str__())
        id += 1

    basic_cohorts = Cohort.objets.all()
    with open('sce/initial_data/subjects.csv', 'rt', encoding='utf8') as f:
        reader = csv.reader(f)
        for row in reader:
            if reader.line_num == 1:
                pass
            else:
                subject = Subject(
                    name=row[1],
                    #key='',
                    #is_active=True,
                    #description='',
                    grade_level=GradeLevel.get(educative_program=EducativeProgram.objects.get(pk=row[5])),
                    category=SubjectCategory.objects.get(pk=row[6]),
                    level=row[7],
                )
                subject.save()
                print('--added subject '+ subject.__str__() + ' in category ' + subject.category.__str__())

    # Marking period
    educative_programs = EducativeProgram.objects.all()
    for educative_program in educative_programs:
        for partial in range(1, 5 + 1):
            marking_period = MarkingPeriod(name='Parcial ' + str(partial),
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
        migrations.RunPython(load_initial_data),
    ]
