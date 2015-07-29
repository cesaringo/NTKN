from .models import Student
from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.contrib.auth.hashers import (
    UNUSABLE_PASSWORD_PREFIX, identify_hasher,
)
from django.utils.html import format_html
from django.forms.utils import flatatt

class ReadOnlyPasswordHashWidget(forms.Widget):
	def render(self, name, value, attrs):
		encoded = value
		final_attrs = self.build_attrs(attrs)

		if not encoded or encoded.startswith(UNUSABLE_PASSWORD_PREFIX):
			summary = mark_safe("<strong>%s</strong>" % ugettext("No password set."))
		else:
			try:
				hasher = identify_hasher(encoded)
			except ValueError:
				summary = mark_safe("<strong>%s</strong>" % ugettext(
					"Invalid password format or unknown hashing algorithm."))

			else:
				summary = format_html_join('',
					"<strong>{}</strong>: {} ",
					((ugettext(key), value)
					for key, value in hasher.safe_summary(encoded).items())
				)

		return format_html("<div{}>{}</div>", flatatt(final_attrs), summary)

class ReadOnlyPasswordHashField(forms.Field):
	widget = ReadOnlyPasswordHashWidget

	def __init__(self, *args, **kwargs):
		kwargs.setdefault("required", False)
		super(ReadOnlyPasswordHashField, self).__init__(*args, **kwargs)

	def bound_data(self, data, initial):
		return initial

	def has_changed(self, initial, data):
		return False


class StudentCreationForm(forms.ModelForm):
	"""
	A form that creates a Student from the given first_name, last_name and password
	"""

	error_messages = {
		'password_mismatch': _("The two password fields didn't match."),
	}
	password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
	password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as before, for verification."))


	class Meta:
		model = Student
		fields = ('first_name', 'last_name', )


	def clean_password2(self):
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError(
				self.error_messages['password_mismatch'],
				code='password_mismatch',
			)
		self.instance.username = self.cleaned_data.get('username') #WTF
		password_validation.validate_password(self.cleaned_data.get('password2'), self.instance)
		return password2


	def save(self, commit=True):
		student = super(StudentCreationForm, self).save(commit=False)
		student.set_password(self.cleaned_data["password1"])
		if commit:
			student.save()
		return student



class StudentChangeForm(forms.ModelForm):
	password = ReadOnlyPasswordHashField(label=_("Password"),
        help_text=_("Raw passwords are not stored, so there is no way to see "
                    "this student's password, but you can change the password "
                    "using <a href=\"../password/\">this form</a>."))

	class Meta:
		model = Student
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		super(StudentChangeForm, self).__init__(*args, **kwargs)
		f = self.fields.get('user_permissions')
		if f is not None:
			f.queryset = f.queryset.select_related('content_type') #WTF

	def clean_password(self):
		return self.initial["password"]
