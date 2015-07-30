from django.contrib import admin
from .models import Student, Course, Subject, EducativeProgram, SchoolYear
from import_export import resources
from import_export.admin import ImportExportMixin
from import_export import fields
from authentication.admin import AccountAdmin

class StudentResource(resources.ModelResource):
	#educative = fields.Field(column_name='myfield')
	class Meta:
		model = Student
		fields = ('id', 'first_name', 'last_name', 'sex', 'bday', 'educative_program',  'first_school_year', 'parent_email', 'parent_phone', 'email')


class StudentAdmin(ImportExportMixin, AccountAdmin):
	resource_class = StudentResource
	list_display = ('get_photo_as_tag', 'enrollment', '__unicode__', 'email_link', 'is_active', 'educative_program')
	list_display_links = ('get_photo_as_tag', 'enrollment', '__unicode__',)

	fieldsets = (
        ('Student', {'fields': (
        	'photo', 'first_name', 'last_name', 
        	'password','sex', 'is_active', 'updated_at', 'created_at'
        	)}),
	)
	readonly_fields = ('updated_at', 'created_at')

	list_filter = ('is_active', 'educative_program')


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

