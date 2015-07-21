from django.contrib import admin
from .models import Student, Course, Subject, EducativeProgram
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class StudentResource(resources.ModelResource):
	class Meta:
		model = Student
		fields = ('id', 'first_name', 'last_name', 'sex', 'bday', 'educative_program',  'parent_email', 'parent_phone')

class StudentAdmin(ImportExportModelAdmin):
	resource_class = StudentResource
	pass


admin.site.register(Student, StudentAdmin)
admin.site.register(Subject)
admin.site.register(Course)
admin.site.register(EducativeProgram)

