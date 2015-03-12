from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings
from datetime import date
from localflavor.us.models import PhoneNumberField
User = get_user_model()

class Student(User):
	mname = models.CharField(max_length=100, blank=True, null=True, vorbose_name="Middle name")
	sex	= models.CharField(max_length=1, choices=(('M', 'Male'), ('F', 'Female')), blank=True, null=True )
	bday = models.DateField(blank=True, null=True, verbose_name="Birth Date", validators=settings.DATE_VALIDATORS)
	year = models.ForeignKey(GradeLevel, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Grade level")
	class_year = models.ForeignKey(ClassYear, verbose_name="Class year", blank=True, null=True)

	#Contact
	phone = PhoneNumberField()
	parent_email = models.EmailField(blank=True, editable=False)
	parent_phone  = PhoneNumberField()

	class Meta:
		permissions = (
			("view_student", "View student"),
			("view_contact_info", "View contact info"),
		)
		ordering = ("last_name", "first_name")

	def __unicode__(self):
		return u"{0}, {1}".format(self.last_name, self.first_name)

	def get_absolute_url():
		pass





class GradeLevel(models.Model):
	number	=	models.IntegerField(verbose_name="Grade number")
	name 	= 	models.CharField(max_length=150, unique=True, verbose_name="Grade name")

	class Meta:
		ordering = (number)

	def __unicode__(self):
		return unicode(self.name)

	@property
	def grade(self):
		return self.number

class ClassYear(models.Model):
	"""	ClassYear such as class of 2015
	"""
	year 	= 	models.IntegerField(unique=True, min_value=2000, max_value=date.today().year + 1, help_text="e.g. 2015")
	name 	= 	models.CharField(max_length=255, help_text="e.g. Class of 2015", blank=True)

	class Meta:
		verbose_name = "Class Year"

	def __unicode__(self):
		return self.name

	def save(self, *args, **kwargs):
		if not self.name:
			self.name = "Class of %s" % (self.year,)
		super(ClassYear, self).save(*args, **kwargs)

