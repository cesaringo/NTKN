from django.db import models
from authentication.models import Account
from localflavor.us.models import PhoneNumberField
from django.core.validators import MaxValueValidator, MinValueValidator



class Institute(models.Model):
	name = models.CharField(max_length=200)

	#Contact Information
	facebook = models.CharField(max_length=200)
	twitter = models.CharField(max_length=200)
	instagram = models.CharField(max_length=200)
	youtube = models.CharField(max_length=200)
	phone = PhoneNumberField(null=True, blank=True)
	email = models.EmailField(blank=True, blank=True)
	address = models.CharField(max_length=200)

	#More data about Institute here...

class EducativeProgram(models.Model):
	name = models.CharField(max_length=100, unique=True)
	slug = models.CharField(max_length=100, unique=True, blank=True)
	order = models.IntegerField(null=True, blank=True)
	institute = models.ForeignKey(Institute)

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

class GradeLevel(models.Model):
	number = models.IntegerField(verbose_name="Grade number")
	name = models.CharField(max_length=100, verbose_name="Grade name", blank=True)
	slug = models.CharField(max_length=100, verbose_name="slug", blank=True)
	educative_program = models.ForeignKey(EducativeProgram)
	order = models.IntegerField(null=True, blank=True)



	class Meta:
		ordering = ('order',)
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

class SchoolYear(models.Model):
	name = models.CharField(max_length=100, unique=True)
	start_date = models.DateField(validators=settings.DATE_VALIDATORS)
	end_date = models.DateField(validators=settings.DATE_VALIDATORS)
	active_year = models.BooleanField(default=False, help_text = '')


	class Meta:
		ordering = ('start_date',)

	def __str__(self):
		return self.name

class Student(Account):
	institute = models.ForeignKey(Institute)
	enrollment = models.CharField(max_length=8, blank=True, null=True) #Primary Id for the institute.

	sex	= models.CharField(max_length=1, choices=(('M', 'Male'), ('F', 'Female')), blank=True, null=True)
	bday = models.DateField(blank=True, null=True, verbose_name="Birth Date", validators=settings.DATE_VALIDATORS)
	class_year = models.ForeignKey(ClassYear, verbose_name="Class year / School Generation", blank=True, null=True)
	grade_level = models.ForeignKey(GradeLevel, blank=True, null=True, on_delete=models.SET_NULL)
	#First School year of any student
	first_school_year = models.ForeignKey(SchoolYear, null=True, on_delete=models.SET_NULL)