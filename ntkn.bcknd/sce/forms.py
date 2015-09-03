from .models import Student, Cohort, Course
from django.contrib.auth.forms import (
    UserChangeForm, UserCreationForm,
)
from django import forms
from django.contrib import admin

class StudentChangeForm(UserChangeForm):
	cohorts = forms.ModelMultipleChoiceField(
		Cohort.objects.all(),
		widget=admin.widgets.FilteredSelectMultiple('Cohort', False),
		required=False,
	)
	
	def __init__(self, *args, **kwargs):
		super(StudentChangeForm, self).__init__(*args, **kwargs)
		if self.instance.pk:
			self.initial['cohorts'] = self.instance.cohort_set.values_list('pk', flat=True)

	def save(self, *args, **kwargs):
		instance = super(StudentChangeForm, self).save(*args, **kwargs)  
		if instance.pk: 
			for cohort in instance.cohort_set.all():
				if cohort not in self.cleaned_data['cohorts']:
					instance.cohort_set.remove(cohort) 
			for cohort in self.cleaned_data['cohorts']:
				if cohort not in instance.cohort_set.all():
					instance.cohort_set.add(cohort)
		return instance




class StudentCreationForm(UserCreationForm):
	pass

class CourseForm(forms.ModelForm):
	class Meta:
		model = Course
		fields = ('subject','school_year', 'teacher', 'cohort', 'is_active', 'marking_periods', 'students')
	pass