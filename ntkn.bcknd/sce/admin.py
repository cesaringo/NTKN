from django.contrib import admin
from .models import Student, Course, Subject

admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(Course)
# Register your models here.

