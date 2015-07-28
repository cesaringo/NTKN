from django.contrib import admin
from .models import Student, Course, Subject, EducativeProgram, SchoolYear
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin
from import_export import fields

class StudentResource(resources.ModelResource):
	#educative = fields.Field(column_name='myfield')
	class Meta:
		model = Student
		fields = ('id', 'first_name', 'last_name', 'sex', 'bday', 'educative_program',  'first_school_year', 'parent_email', 'parent_phone', 'email')


class StudentAdmin(ImportExportActionModelAdmin):
	resource_class = StudentResource
	pass


class EcucativeProgramAdmin(admin.ModelAdmin):
	list_display = ('id','__unicode__',)
	list_display_links = ('id','__unicode__',)
	ordering = ['id']

class SchoolYearAdmin(admin.ModelAdmin):
	list_display = ('id','__unicode__', 'start_date', 'end_date',)
	ordering = ['id']
		
admin.site.register(Student, StudentAdmin)
admin.site.register(Subject)
admin.site.register(Course)
admin.site.register(EducativeProgram, EcucativeProgramAdmin)
admin.site.register(SchoolYear, SchoolYearAdmin)

