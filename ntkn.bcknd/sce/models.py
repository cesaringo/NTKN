from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import models
from django.conf import settings
from datetime import date
from localflavor.us.models import PhoneNumberField
from authentication.models import Account
from slugify import slugify
from datetime import datetime


################
#Students Module
################

#Periodo escolar
class SchoolYear(models.Model):
	name = models.CharField(max_length=100, unique=True)
	start_date = models.DateField(validators=settings.DATE_VALIDATORS)
	end_date = models.DateField(validators=settings.DATE_VALIDATORS)
	active_year = models.BooleanField(default=False, help_text = '')

	class Meta:
		ordering = ('start_date',)

	def __unicode__(self):
		return self.name


class GradeLevel(models.Model):
	number	=	models.IntegerField(verbose_name="Grade number")
	name 	= 	models.CharField(max_length=150, unique=True, verbose_name="Grade name")

	class Meta:
		ordering = ('number',)

	def __unicode__(self):
		return unicode(self.name)

	@property
	def grade(self):
		return self.number

class IntegerRangeField(models.IntegerField):
	def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
		self.min_value, self.max_value = min_value, max_value
		models.IntegerField.__init__(self, verbose_name, name, **kwargs)

	def formfield(self, **kwargs):
		defaults = {'min_value': self.min_value, 'max_value':self.max_value}
		defaults.update(kwargs)
		return super(IntegerRangeField, self).formfield(**defaults)

class ClassYear(models.Model):
	"""	ClassYear such as class of 2015
	"""
	year 	= 	IntegerRangeField(unique=True, min_value=2000, max_value=date.today().year + 1, help_text="e.g. 2015")
	name 	= 	models.CharField(max_length=255, help_text="e.g. Class of 2015", blank=True)

	class Meta:
		verbose_name = "Class Year"

	def __unicode__(self):
		return self.name

	def save(self, *args, **kwargs):
		if not self.name:
			self.name = "Class of %s" % (self.year,)
		super(ClassYear, self).save(*args, **kwargs)



## SUch Ass Preescolar, Primaria, Secundaria, Preparatoria
class EducativeProgram(models.Model):
	name = models.CharField(max_length=100, unique=True)
	slug = models.CharField(max_length=100, unique=True, blank=True)
	
	def __unicode__(self):
		return self.name

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug =  slugify(self.name, to_lower=True)
		super(EducativeProgram, self).save(*args, **kwargs)

	
#A group od Students. For this purpose is A, B, C even english levelss
class Cohort(models.Model):
	name = models.CharField(max_length=255)
	students = models.ManyToManyField('Student', blank=True)
	class Meta:
		ordering = ('name',)
	
	def __unicode__(self):
		return self.name

class Student(Account):
	mname = models.CharField(max_length=100, blank=True, null=True, verbose_name="Middle name")
	sex	= models.CharField(max_length=1, choices=(('M', 'Male'), ('F', 'Female')), blank=True, null=True )
	bday = models.DateField(blank=True, null=True, verbose_name="Birth Date", validators=settings.DATE_VALIDATORS)

	#The student enrollment
	enrollment = models.CharField(max_length=8, blank=True, null=True)

	#The current student Grade Level. 
	#Preescolar (3), Primaria (6), Secundaria (3), Preparatoria (3)
	year = models.ForeignKey(GradeLevel, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Grade level")
	
	#The years the student is expected starting and ending 
	class_year = models.ForeignKey(ClassYear, verbose_name="Class year / School Generation", blank=True, null=True)
	

	#The current educative program the student is coursing 
	educative_program = models.ForeignKey(EducativeProgram, blank=True, null=True, on_delete=models.SET_NULL)

	#First School year of any student
	first_school_year = models.ForeignKey(SchoolYear, null=True, on_delete=models.SET_NULL)

	#Contact
	phone = PhoneNumberField(null=True, blank=True)
	parent_email = models.EmailField(blank=True, editable=False)
	parent_phone  = PhoneNumberField(null=True, blank=True)
	
	cohorts = models.ManyToManyField(Cohort, blank=True)

	class Meta:
		permissions = (
			("view_student", "View student"),
			("view_contact_info", "View contact info"),
		)
		ordering = ("last_name", "first_name")

	def __unicode__(self):
		if self.first_name or self.last_name:
			return u"{0}, {1}".format(self.last_name, self.first_name)
		else:
			return "Student " + str(self.id)

	def get_absolute_url():
		pass

	def save(self, *args, **kwargs):
		group = Group.objects.get(name="student")
		self.groups.add(group)

		if self.id is None:
			super(Student, self).save(*args, **kwargs)
			self.save(*args, **kwargs)
		else:
			self.username = '{0:07}'.format(self.id + 1000000)
			self.email = self.username + '@natkan.mx'
			if self.first_school_year:
				self.enrollment = str(datetime.now().year % 100) + '{0:02d}'.format(datetime.now().month) + '{0:02d}'.format(self.first_school_year.id % 100) + '{0:02}'.format(self.id)
			super(Student, self).save(*args, **kwargs)


class Teacher(Account):
	phone = PhoneNumberField()
	##Adtional administrative data for teacher

	def __str__(self):
		return self.get_full_name()

	def save(self, *args, **kwargs):
		group = Group.objects.get(name="teacher")
		self.groups.add(group)
		super(Teacher, self).save(*args, **kwargs)






################
#schedule module
################
class Department(models.Model):
	name = models.CharField(max_length=255, unique=True, verbose_name="Department Name")


#Ejemplo: Bimestre 1, Bimestre 2, Parcila 1, Parcial 2, etc
class MarkingPeriod(models.Model):
	name = models.CharField(max_length=255, unique=True)
	shortname = models.CharField(max_length=255)
	start_date = models.DateField()
	end_date = models.DateField()
	grades_due = models.DateField(validators=settings.DATE_VALIDATORS, blank=True, null=True, help_text="If filled out, teachers will be notified when grades are due.")
	active = models.BooleanField(default=False, help_text="Teachers may only enter grades for active marking periods. There may be more than one active marking period.")

	class Meta:
		ordering = ('-start_date',)

	def __unicode__(self):
		return self.name

class Subject(models.Model):
	is_active = models.BooleanField(default=True)
	fullname = models.CharField(max_length=255, unique=True, verbose_name="Full Course Name")
	shortname = models.CharField(max_length=255, verbose_name="Short Name")
	graded = models.BooleanField(default=True, help_text="Teachers can submit grades for this course")
	description = models.TextField(blank=True)
	level = models.ForeignKey(GradeLevel, blank=True, null=True, verbose_name="Grade Level")
	department = models.ForeignKey(Department, blank=True, null=True)

	def __unicode__(self):
		return self.fullnames


class Course(models.Model):
	subject = models.ForeignKey(Subject, related_name='courses')
	is_active = models.BooleanField(default=True)
	name = models.CharField(max_length=255, null=True)
	#Periodos de evaluacion
	marking_period = models.ManyToManyField(MarkingPeriod, blank=True)
	teacher = models.ForeignKey(Teacher, blank=True)
	school_year = models.ForeignKey(SchoolYear)

	def __unicode__(self):
		return self.fullname


class CourseEnrollment(models.Model):
	student = models.ForeignKey(Student)
	course = models.ForeignKey(Course)
	is_active = models.BooleanField(default=True)
	
	class Meta:
		unique_together =  (("course", "student"),)


	def get_average_for_marking_periods():
		pass





##################
#Discipline Module
##################





##################
#Attendance Module
##################