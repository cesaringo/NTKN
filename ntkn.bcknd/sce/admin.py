from django.contrib import admin
from .models import Student, Course, Subject, EducativeProgram, SchoolYear, Teacher, SubjectCategory, Cohort
from import_export import resources
from import_export.admin import ImportExportMixin
from import_export import fields
from authentication.admin import AccountAdmin
from .forms import StudentChangeForm, StudentCreationForm

class StudentResource(resources.ModelResource):
	#educative = fields.Field(column_name='myfield')
	class Meta:
		model = Student
		fields = ('id', 'first_name', 'last_name', 'sex', 'bday', 'educative_program',  'first_school_year', 'parent_email', 'parent_phone', 'email')


class StudentAdmin(ImportExportMixin, AccountAdmin):
	resource_class = StudentResource
	list_display = ('get_photo_as_tag', 'enrollment', '__str__', 'email_link', 'is_active', 'educative_program')
	list_display_links = ('get_photo_as_tag', 'enrollment', '__str__',)

	fieldsets = (
        ('User Info', {'fields': (
        	'photo', 'first_name', 'last_name', 'enrollment',	'username', 'email',
        	'password','sex', 'is_active', 'updated_at', 'created_at'
        	)}),

        ('Student Info', {'fields': (
        	'educative_program', 'cohorts'
        	)}),

        ("Contact", {'fields': (
        	'phone', 'parent_phone', 'parent_email', 
        	)}),

	)
	readonly_fields = ('updated_at', 'created_at')

	list_filter = ('is_active', 'educative_program')

	#AdminForms
	form = StudentChangeForm
	add_form = StudentCreationForm

class TeacherAdmin(AccountAdmin):
	list_display = ('get_photo_as_tag', '__str__', 'email_link', 'is_active', )
	list_display_links = ('get_photo_as_tag', '__str__',)
	fieldsets = (
        ('Student', {'fields': (
        	'photo', 'first_name', 'last_name', 'email',
        	'password', 'is_active', 'updated_at', 'created_at'
        	)}),
	)
	readonly_fields = ('updated_at', 'created_at')

class EcucativeProgramAdmin(admin.ModelAdmin):
	list_display = ('id','__unicode__',)
	list_display_links = ('id','__unicode__',)
	ordering = ['id']

class SchoolYearAdmin(admin.ModelAdmin):
	list_display = ('id','__str__', 'start_date', 'end_date',)
	ordering = ['id']
		

class SubjectResource(resources.ModelResource):
	class Meta:
		model = Subject
		fields = ('id', 'fullname', 'key', 'is_active', 'description', 'educative_program', 'category', 'levels')

class SubjectAdmin(ImportExportMixin, admin.ModelAdmin):
	resource_class = SubjectResource
	list_display = ('shortname', 'fullname', 'educative_program', 'is_active')
	list_display_links = ('shortname', 'fullname',)
	ordering = ('educative_program',)

	fieldsets = (
		(None, {'fields': ('fullname', 'shortname', 'description',)}), 
		(None, {'fields': ('is_active', 'educative_program', 'category', 'graded',  'levels')}),
	)

	list_filter = ('is_active', 'educative_program')

class SubjectCategoryAdmin(admin.ModelAdmin):
	pass
		

class CohortAdmin(admin.ModelAdmin):
	filter_horizontal = ('students',)


	

admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(SubjectCategory, SubjectCategoryAdmin)
admin.site.register(Course)
admin.site.register(Cohort, CohortAdmin)
admin.site.register(EducativeProgram, EcucativeProgramAdmin)
admin.site.register(SchoolYear, SchoolYearAdmin)


