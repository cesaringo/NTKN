from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import models
from django.conf import settings
from datetime import date
from localflavor.us.models import PhoneNumberField
from authentication.models import Account
from django.utils.text import slugify
from datetime import datetime
from django.core import urlresolvers
from django.db.models import Sum
from decimal import *
from django.core.validators import MaxValueValidator, MinValueValidator

################
#Students Module
#################

#Periodo escolar
class SchoolYear(models.Model):
	name = models.CharField(max_length=100, unique=True)
	start_date = models.DateField(validators=settings.DATE_VALIDATORS)
	end_date = models.DateField(validators=settings.DATE_VALIDATORS)
	active_year = models.BooleanField(default=False, help_text = '')
	

	class Meta:
		ordering = ('start_date',)

	def __str__(self):
		return self.name


class GradeLevel(models.Model):
	number = models.IntegerField(verbose_name="Grade number")
	educative_program = models.ForeignKey('EducativeProgram')
	name = models.CharField(max_length=100, verbose_name="Grade name", blank=True)
	order = models.IntegerField(null=True, blank=True)
	slug = models.CharField(max_length=100, verbose_name="slug", blank=True)


	class Meta:
		ordering = ('number',)
		unique_together =  (('number', 'educative_program'),)

	def __unicode__(self):
		return unicode(self.name)

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
	order = models.IntegerField(null=True, blank=True)
	marking_periods = models.IntegerField()

	def __unicode__(self):
		return self.name

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug =  slugify(self.name, to_lower=True)
		super(EducativeProgram, self).save(*args, **kwargs)

	


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
	parent_email = models.EmailField(blank=True, )
	parent_phone  = PhoneNumberField(null=True, blank=True)
	

	class Meta:
		permissions = (
			("view_student", "View student"),
			("view_contact_info", "View contact info"),
		)
		ordering = ("last_name", "first_name")

	def __str__(self):
		if self.first_name or self.last_name:
			return u"{0}, {1}".format(self.last_name, self.first_name)
		elif self.email:
			return self.email
		else:
			return "Student " + str(self.id)

	def get_absolute_url():
		pass

	def save(self, *args, **kwargs):
		if self.id is None:
			super(Student, self).save(*args, **kwargs)
			self.save(*args, **kwargs)
		else:
			group = Group.objects.get(name="student")
			self.groups.add(group)
			self.username = '{0:07}'.format(self.id + 1000000)
			self.email = self.username + '@natkan.mx'
			if self.first_school_year:
				self.enrollment = str(datetime.now().year % 100) + '{0:02d}'.format(datetime.now().month) + '{0:02d}'.format(self.first_school_year.id % 100) + '{0:02}'.format(self.id)
			super(Student, self).save(*args, **kwargs)

#A group od Students. For this purpose is A, B, C even english levelss
class Cohort(models.Model):
	name = models.CharField(max_length=255)
	students = models.ManyToManyField(
		Student, 
		blank=True,
		related_name = 'cohorts',
		related_query_name = 'cohort'
	)
	class Meta:
		ordering = ('name',)
	
	def __str__(self):
		return self.name

class Teacher(Account):
	phone = PhoneNumberField()
	##Adtional administrative data for teacher

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



################
#schedule module
################
class Department(models.Model):
	name = models.CharField(max_length=255, unique=True, verbose_name="Department Name")




#Categoria de las asignaturas como por ejemplo las asignaturas de kinder. Sirve para tener una manera de agruparlas
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

	#level of the subject. Math 1, Math 2, etc
	level = models.IntegerField(null=True)

	#The Grade Level the subject is suposed to be imparted
	grade_level = models.ForeignKey(GradeLevel, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Grade level")

	department = models.ForeignKey(Department, blank=True, null=True)

	#La educacion basica (Preescolar, primaria, Segundaria) cuenta con 4 peridos escolares
	#primer periodo preescolar, Segundo y tercer periodo primaria, cuarto periodo secundaria
	#List of ints
	periods = models.CommaSeparatedIntegerField(max_length=100, blank=True)


	#Some subjects are grouped by category
	category = models.ForeignKey(SubjectCategory, null=True, blank=True, default=None)

	#The educative program the subject is associated 
	educative_program = models.ForeignKey(EducativeProgram, blank=True, null=True, on_delete=models.SET_NULL)

	order = models.IntegerField(null=True)


	def __str__(self):
		return self.fullname + ' ' + str(self.level)

#Ejemplo: Bimestre 1, Bimestre 2, Parcila 1, Parcial 2, etc
class MarkingPeriod(models.Model):
	name = models.CharField(max_length=255, unique=True)
	shortname = models.CharField(max_length=255)
	description = models.TextField(null=True, blank=True)
	start_date = models.DateField()
	end_date = models.DateField()
	grades_due = models.DateField(validators=settings.DATE_VALIDATORS, blank=True, null=True, help_text="If filled out, teachers will be notified when grades are due.")
	active = models.BooleanField(default=False, help_text="Teachers may only enter grades for active marking periods. There may be more than one active marking period.")

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
		related_query_name = 'course',
	)

	students = models.ManyToManyField(
		Student,
		through='CourseEnrollment',
		blank = True,
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

	def save(self, *args, **kwargs):
		if self.pk is not None:
			orig = Course.objects.get(pk=self.pk)
			if Course.marking_periods != self.marking_periods:
				related_course_enrollments = CourseEnrollment.objects.filter(course=self)
				for course_enrollment in related_course_enrollments:
					course_enrollment.ma

		super(Course, self).save(*args, **kwargs)





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
		unique_together =  (("course", "student"),)


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


	def get_avarage(self):
		n = Decimal(self.scores.count())
		x = Decimal(0)
		for s in self.scores.all():
			if s.score is None:
				return None
			x += s.score

		if n is None or x is None:
			return None
		return x/n
		
		

class Score(models.Model):
	score = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True, 
		validators = [MinValueValidator(0.0), MaxValueValidator(10.0)])
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


##################
#Discipline Module
##################





##################
#Attendance Module
##################