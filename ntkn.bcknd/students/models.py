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


class Student(Account):
	institute = models.ForeignKey(Institute)
	enrollment = models.CharField(max_length=8, blank=True, null=True) #Primary Id for the institute.

	sex	= models.CharField(max_length=1, choices=(('M', 'Male'), ('F', 'Female')), blank=True, null=True)
	bday = models.DateField(blank=True, null=True, verbose_name="Birth Date", validators=settings.DATE_VALIDATORS)

	current_educative_program = models.ForeignKey(EducativeProgram, null=True, on_delete=models.SET_NULL)
	