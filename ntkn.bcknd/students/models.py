from datetime import date, datetime
from django.db import models

from authentication.models import Account
from localflavor.us.models import PhoneNumberField
from django.contrib.auth.models import Group
from slugify import slugify
from ntkn import settings


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

    def __str__(self):
        return self.name
        # More data about Institute here...


class EducativeProgram(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.CharField(max_length=100, unique=True, blank=True)
    marking_periods = models.IntegerField()
    num_of_levels = models.IntegerField()
    institute = models.ForeignKey(Institute)

    order = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


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

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = "Class of %s" % (self.year,)
        super(ClassYear, self).save(*args, **kwargs)


class GradeLevel(models.Model):
    number = models.IntegerField(verbose_name="Grade number")
    name = models.CharField(max_length=100, verbose_name="Grade name", blank=True)
    slug = models.CharField(max_length=100, verbose_name="slug", blank=True)
    educative_program = models.ForeignKey(EducativeProgram)
    order = models.IntegerField(null=True, blank=True)

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
        self.slug = slugify(self.name)
        super(GradeLevel, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class SchoolYear(models.Model):
    name = models.CharField(max_length=100, unique=True)
    start_date = models.DateField(validators=settings.DATE_VALIDATORS)
    end_date = models.DateField(validators=settings.DATE_VALIDATORS)
    active_year = models.BooleanField(default=False, help_text='')

    class Meta:
        ordering = ('start_date',)

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
    first_school_year = models.ForeignKey(SchoolYear, null=True, on_delete=models.SET_NULL)
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
            if self.first_school_year:
                self.enrollment = str(datetime.now().year % 100) + '{0:02d}'.format(
                    datetime.now().month) + '{0:02d}'.format(self.first_school_year.id % 100) + '{0:02}'.format(self.id)
            super(Student, self).save(*args, **kwargs)
