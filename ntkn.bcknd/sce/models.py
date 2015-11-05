from django.contrib.auth.models import Group
from django.db import models
from django.conf import settings
from localflavor.us.models import PhoneNumberField
from authentication.models import Account
from django.core import urlresolvers
from decimal import *
from django.core.validators import MaxValueValidator, MinValueValidator
from slugify import slugify
from students.models import Student, Teacher, GradeLevel, EducativeProgram


class SchoolYear(models.Model):
    name = models.CharField(max_length=100, unique=True)
    start_date = models.DateField(validators=settings.DATE_VALIDATORS)
    end_date = models.DateField(validators=settings.DATE_VALIDATORS)
    active_year = models.BooleanField(default=False, help_text='')

    class Meta:
        ordering = ('start_date',)

    def __str__(self):
        return self.name


class Cohort(models.Model):
    name = models.CharField(max_length=255)
    students = models.ManyToManyField(
        Student,
        blank=True,
        related_name='cohorts',
        related_query_name='cohort'
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Department Name")


class SubjectCategory(models.Model):
    name = models.CharField(max_length=150)
    order = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class Subject(models.Model):
    is_active = models.BooleanField(default=True)
    fullname = models.CharField(max_length=255, verbose_name="Subject Name")
    shortname = models.CharField(max_length=255, verbose_name="Key")
    graded = models.BooleanField(default=True, help_text="Teachers can submit grades for this course")
    description = models.TextField(null=True, blank=True)

    # level of the subject. Math 1, Math 2, etc
    level = models.IntegerField(null=True)

    # The Grade Level the subject is supposed to be imparted
    grade_level = models.ForeignKey(GradeLevel, blank=True, null=True, on_delete=models.SET_NULL,
                                    verbose_name="Grade level")

    department = models.ForeignKey(Department, blank=True, null=True)

    # Some subjects are grouped by category
    category = models.ForeignKey(SubjectCategory, null=True, blank=True, default=None)

    # The educative program the subject is associated.
    # Educative program can be retrieved from grade_level.educative_program
    educative_program = models.ForeignKey(EducativeProgram, blank=True, null=True, on_delete=models.SET_NULL)

    order = models.IntegerField(null=True)

    def __str__(self):
        return self.fullname + ' ' + str(self.level)


class MarkingPeriod(models.Model):
    name = models.CharField(max_length=255, unique=True)
    shortname = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    grades_due = models.DateField(
        validators=settings.DATE_VALIDATORS, blank=True, null=True,
        help_text="If filled out, teachers will be notified when grades are due.")
    active = models.BooleanField(
        default=False,
        help_text="Teachers may only enter grades for active marking periods. "
                  "There may be more than one active marking period.")

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
    cohort = models.ForeignKey(Cohort, null=True, blank=True)

    def __str__(self):
        return self.subject.__str__()

    def grade_level(self):
        return self.subject.grade_level


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

    def get_average_for_marking_periods():
        pass

    def __str__(self):
        return '(' + self.student.__str__() + ' - ' + self.course.__str__() + ')'

    def save(self, *args, **kwargs):
        create_scores = False
        if self.pk is None:
            create_scores = True
        super(CourseEnrollment, self).save(*args, **kwargs)
        if create_scores:
            for marking_period in self.course.marking_periods.all():
                print(marking_period)
                score = Score(marking_period=marking_period, course_enrollment=self)
                score.save()

    def get_average(self):
        n = Decimal(self.scores.count())
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


