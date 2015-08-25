from .models import Student
from django.contrib.auth.forms import (
    UserChangeForm, UserCreationForm,
)


class StudentChangeForm(UserChangeForm):
	pass


class StudentCreationForm(UserCreationForm):
	pass