from django.db import models
from django.conf import settings
from django.core import urlresolvers
from decimal import *
from django.core.validators import MaxValueValidator, MinValueValidator
from slugify import slugify
from authentication.models import Account
from localflavor.us.models import PhoneNumberField
from datetime import date, datetime
from django.contrib.auth.models import Group


class Institute(models.Model):
    name = models.CharField(max_length=200)

    # Contact Information
    facebook = models.CharField(max_length=200, null=True, blank=True)
    twitter = models.CharField(max_length=200, null=True, blank=True)
    instagram = models.CharField(max_length=200, null=True, blank=True)
    youtube = models.CharField(max_length=200, null=True, blank=True)
    phone = PhoneNumberField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    order = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
        # More data about Institute here...


class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value': self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)


class ClassYear(models.Model):
    """	ClassYear such as class of 2015"""
    year = IntegerRangeField(unique=True, min_value=2000, max_value=date.today().year + 1, help_text="e.g. 2015")
    name = models.CharField(max_length=255, help_text="e.g. Class of 2015", blank=True)

    class Meta:
        verbose_name = "Class Year"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = "Class of %s" % (self.year,)
        super(ClassYear, self).save(*args, **kwargs)


class EducativeProgram(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.CharField(max_length=100, unique=True, blank=True)
    institute = models.ForeignKey(Institute)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(null=True, blank=True)

    def get_subjects(self):
        grade_levels_id = self.gradelevel_set.all().values_list('id', flat=True)
        subjects = Subject.objects.filter(grade_level_id__in=grade_levels_id)
        return subjects

    def __str__(self):
        return self.name


class GradeLevel(models.Model):
    number = models.IntegerField(verbose_name="Grade number")
    name = models.CharField(max_length=100, verbose_name="Grade name", blank=True)
    slug = models.CharField(max_length=100, verbose_name="slug", blank=True)
    order = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    educative_program = models.ForeignKey(EducativeProgram)

    def get_subjects(self):
        return self.subject_set.all()

    def get_cohorts(self):
        return self.cohort_set.all()

    class Meta:
        ordering = ('order',)
        unique_together = (('number', 'educative_program'),)

    def __str__(self):
        return self.name

    @property
    def grade(self):
        return self.number

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = str(self.number) + ' ' + self.educative_program.name
        self.slug = slugify(self.name + self.educative_program.__str__())
        super(GradeLevel, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Student(Account):
    institute = models.ForeignKey(Institute)
    enrollment = models.CharField(max_length=8, blank=True, null=True)  # Primary Id for the institute.

    sex = models.CharField(max_length=1, choices=(('M', 'Male'), ('F', 'Female')), blank=True, null=True)
    birthday = models.DateField(blank=True, null=True, verbose_name="Birth Date", validators=settings.DATE_VALIDATORS)
    class_year = models.ForeignKey(ClassYear, verbose_name="Class year / School Generation", blank=True, null=True)
    grade_level = models.ForeignKey(GradeLevel, blank=True, null=True, on_delete=models.SET_NULL)
    # First School year of any student
    #first_school_year = models.ForeignKey(SchoolYear, null=True, on_delete=models.SET_NULL)
    phone = PhoneNumberField(null=True, blank=True)
    parent_email = models.EmailField(null=True, blank=True)
    parent_phone = PhoneNumberField(null=True, blank=True)

    class Meta:
        ordering = ('last_name', 'first_name')

    def __str__(self):
        if self.first_name or self.last_name:
            return u"{0}, {1}".format(self.last_name, self.first_name)
        elif self.email:
            return self.email
        else:
            return "Student " + str(self.id)

    def get_absolute_url(self):
        pass

    def save(self, *args, **kwargs):
        if self.id is None:
            super(Student, self).save(*args, **kwargs)
            self.save(*args, **kwargs)
        else:
            group = Group.objects.get(name='student')
            self.groups.add(group)
            self.username = '{0:07}'.format(self.id + 1000000)
            self.email = self.username + '@natkan.mx'
            self.enrollment = self.username
            #if self.first_school_year:
            #    self.enrollment = str(datetime.now().year % 100) + '{0:02d}'.format(
            #        datetime.now().month) + '{0:02d}'.format(self.first_school_year.id % 100) + '{0:02}'.format(self.id)
            #print(type(self.password))
            if self.password is "":
                self.set_password(self.username)
                super(self.__class__, self).set_password(self.username)
            else:
                self.set_password(self.password)
                super(self.__class__, self).set_password(self.password)
            super(self.__class__, self).save()
            super(Student, self).save(*args, **kwargs)
            return self.id


class Teacher(Account):
    phone = PhoneNumberField()

    def __str__(self):
        if self.get_full_name():
            return self.get_full_name()

    def save(self, *args, **kwargs):
        if self.id is None:
            super(Teacher, self).save(*args, **kwargs)
            self.save(*args, **kwargs)
        else:
            group = Group.objects.get(name="teacher")
            self.groups.add(group)

            self.username = '{0:07}'.format(self.id + 1000000)
            self.email = self.username + '@natkan.mx'
            super(Teacher, self).save(*args, **kwargs)


class Cohort(models.Model):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    students = models.ManyToManyField(
        Student,
        blank=True,
        related_name='cohorts',
        related_query_name='cohort'
    )
    grade_levels = models.ManyToManyField(
        GradeLevel,
        blank=True,
        #related_name='cohorts',
        related_query_name='cohort'
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class SchoolYear(models.Model):
    start_date = models.DateField(validators=settings.DATE_VALIDATORS)
    end_date = models.DateField(validators=settings.DATE_VALIDATORS)
    is_active = models.BooleanField(default=False, help_text='')
    educative_program = models.ForeignKey(EducativeProgram)
    slug = models.CharField(max_length=100, unique=True, blank=True)

    class Meta:
        ordering = ('start_date',)

    def __str__(self):
        return self.slug

    def num_of_courses(self):
        return self.course_set.all().count()

    def save(self, *args, **kwargs):
        print ('saving')
        self.slug = slugify('{0}-{1}-{2}'.format(self.educative_program, self.start_date.year, self.end_date.year))
        super(SchoolYear, self).save(*args, **kwargs)


class Department(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Department Name")


class SubjectCategory(models.Model):
    name = models.CharField(max_length=150)
    order = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class Subject(models.Model):
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=255, verbose_name="Subject Name")
    code = models.CharField(max_length=255, verbose_name="Key")
    graded = models.BooleanField(default=True, help_text="Teachers can submit grades for this course")
    description = models.TextField(null=True, blank=True)
    level = models.IntegerField(null=True) # level of the subject. Math 1, Math 2, etc
    grade_level = models.ForeignKey(GradeLevel, blank=True, null=True, on_delete=models.SET_NULL,
                                    verbose_name="Grade level") # The Grade Level the subject is supposed to be imparted
    department = models.ForeignKey(Department, blank=True, null=True)
    category = models.ForeignKey(SubjectCategory, null=True, blank=True, default=None)# Some subjects are grouped by category
    order = models.IntegerField(null=True)

    def __str__(self):
        return self.name + ' ' + str(self.level)


class MarkingPeriod(models.Model):
    name = models.CharField(max_length=255)
    shortname = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    grades_due = models.DateField(
        validators=settings.DATE_VALIDATORS, blank=True, null=True,
        help_text="If filled out, teachers will be notified when grades are due.")
    is_active = models.BooleanField(
        default=False,
        help_text="Teachers may only enter grades for active marking periods. "
                  "There may be more than one active marking period.")

    educative_program = models.ForeignKey(EducativeProgram)

    class Meta:
        ordering = ('shortname',)

    def __str__(self):
        return self.name


class Course(models.Model):
    subject = models.ForeignKey(Subject, related_name='courses')
    teacher = models.ForeignKey(Teacher, blank=True, null=True)
    marking_periods = models.ManyToManyField(
        MarkingPeriod,
        blank=True,
        related_name='course_set',
        related_query_name='course',
    )

    students = models.ManyToManyField(
        Student,
        through='CourseEnrollment',
        blank=True,
        related_name='course_set',
        related_query_name='course'
    )

    name = models.CharField(max_length=255, null=True)
    is_active = models.BooleanField(default=True)
    school_year = models.ForeignKey(SchoolYear)
    cohort = models.ForeignKey(Cohort)

    def __str__(self):
        return self.subject.__str__()

    def grade_level(self):
        return self.subject.grade_level

    class Meta:
        #unique_together = ('subject__id', 'school_year__id', 'cohort__id')
        pass

    def get_marking_periods(self):
        return self.marking_periods.all()

    def save(self, *args, **kwargs):
        super(Course, self).save(*args, **kwargs)
        marking_periods = self.subject.grade_level.educative_program.markingperiod_set.all()
        #print(marking_periods)
        for marking_period in marking_periods:
            self.marking_periods.add(marking_period)


class CourseEnrollment(models.Model):
    student = models.ForeignKey(Student)
    course = models.ForeignKey(Course)
    is_active = models.BooleanField(default=True)

    def changeform_link(self):
        if self.id:
            changeform_url = urlresolvers.reverse(
                'admin:sce_courseenrollment_change', args=(self.id,)
            )
            return u'<a href="%s" target="_blank">Details</a>' % changeform_url
        return u''

    changeform_link.allow_tags = True
    changeform_link.short_description = ''

    class Meta:
        unique_together = (("course", "student"),)

    def get_average_for_marking_periods(self):
        pass

    def __str__(self):
        return '(' + self.student.__str__() + ' - ' + self.course.__str__() + ')'

    def save(self, *args, **kwargs):
        create_scores = False
        if self.pk is None:
            create_scores = True
        super(CourseEnrollment, self).save(*args, **kwargs)
        if create_scores:
            marking_periods = self.course.subject.grade_level.educative_program.markingperiod_set.all()
            scores = []
            for marking_period in marking_periods:
                scores.append(
                    Score(marking_period=marking_period, course_enrollment=self)
                )
                #score.save()
            Score.objects.bulk_create(scores)

    def get_average(self):
        n = Decimal(self.scores.count())
        if n == 0: return None
        x = Decimal(0)
        for s in self.scores.all():
            if s.score is None:
                return None
            x += s.score

        if n is None or x is None:
            return None
        return x / n


class Score(models.Model):
    score = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True,
                                validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])
    marking_period = models.ForeignKey(MarkingPeriod, blank=True, null=True, on_delete=models.SET_NULL)
    course_enrollment = models.ForeignKey(CourseEnrollment,
                                          related_name='scores', related_query_name='score', on_delete=models.CASCADE)

    def __str__(self):
        if self.marking_period:
            return self.marking_period.name
        else:
            return ""

    class Meta:
        ordering = ('marking_period',)


