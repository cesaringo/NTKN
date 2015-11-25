from django.contrib import admin
from sce.models import (EducativeProgram, Course, Subject, SchoolYear, SubjectCategory, Cohort, MarkingPeriod, CourseEnrollment,
                        Score)
from alumni.models import (GradeLevel, Student, Teacher)
from import_export import resources
from import_export.admin import ImportExportMixin
from authentication.admin import AccountAdmin
from sce.forms import StudentChangeForm, StudentCreationForm, CourseForm


class ScoreInline(admin.StackedInline):
    model = Score


class CourseEnrollmentAdmin(admin.ModelAdmin):
    inlines = (ScoreInline,)


class CourseEnrollmentLinkInline(admin.TabularInline):
    model = CourseEnrollment
    fields = ('course', 'is_active', 'changeform_link')
    readonly_fields = ('changeform_link',)


class StudentResource(resources.ModelResource):
    # educative = fields.Field(column_name='myfield')
    class Meta:
        model = Student
        fields = (
            'id', 'first_name', 'last_name', 'sex', 'birthday', 'grade_level', 'first_school_year', 'parent_email',
            'parent_phone', 'email')


class StudentAdmin(ImportExportMixin, AccountAdmin):
    resource_class = StudentResource
    list_display = ('get_photo_as_tag', 'enrollment', '__str__', 'email_link', 'is_active', 'grade_level')
    list_display_links = ('get_photo_as_tag', 'enrollment', '__str__',)

    fieldsets = (
        ('User Info', {'fields': (
            'photo', 'first_name', 'last_name', 'enrollment', 'username', 'email',
            'password', 'sex', 'is_active', 'updated_at', 'created_at'
        )}),

        ('Student Info', {'fields': (
            'cohorts',
        )}),

        ("Contact", {'fields': (
            'phone', 'parent_phone', 'parent_email',
        )}),
    )
    readonly_fields = ('updated_at', 'created_at')

    list_filter = ('is_active', 'grade_level')

    # AdminForms
    form = StudentChangeForm
    add_form = StudentCreationForm

    inlines = (CourseEnrollmentLinkInline,)


class TeacherAdmin(AccountAdmin):
    list_display = ('get_photo_as_tag', '__str__', 'email_link', 'is_active',)
    list_display_links = ('get_photo_as_tag', '__str__',)
    fieldsets = (
        ('Student', {'fields': (
            'photo', 'first_name', 'last_name', 'email',
            'password', 'is_active', 'updated_at', 'created_at'
        )}),
    )
    readonly_fields = ('updated_at', 'created_at')


class EcucativeProgramAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__',)
    list_display_links = ('id', '__str__',)
    ordering = ['id']


class SchoolYearAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__', 'start_date', 'end_date', 'is_active')
    ordering = ['id']


class SubjectResource(resources.ModelResource):
    class Meta:
        model = Subject
        fields = (
            'id', 'fullname', 'key', 'is_active', 'description', 'educative_program', 'category', 'level',
            'grade_level')


class SubjectAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = SubjectResource
    list_display = ('shortname', '__str__', 'educative_program', 'level', 'grade_level', 'is_active', 'get_cohorts')
    list_display_links = ('shortname', '__str__',)
    ordering = ('educative_program',)

    fieldsets = (
        (None, {'fields': ('fullname', 'shortname', 'description',)}),
        (None, {'fields': ('is_active', 'educative_program', 'category', 'graded', 'level', 'grade_level', 'cohorts')}),
    )

    list_filter = ('is_active', 'educative_program', 'grade_level', 'grade_level')


class SubjectCategoryAdmin(admin.ModelAdmin):
    pass


class CohortAdmin(admin.ModelAdmin):
    filter_horizontal = ('students',)


class MarkingPeriodAdmin(admin.ModelAdmin):
    list_display = ('name', 'shortname', 'active', 'description')
    ordering = ('name',)


class CourseAdmin(admin.ModelAdmin):
    filter_horizontal = ('marking_periods', 'students',)
    form = CourseForm
    inlines = (CourseEnrollmentLinkInline,)
    list_display = ('id', 'subject', 'teacher', 'grade_level', 'cohort', 'school_year', 'is_active',)
    list_display_links = ('id', 'subject',)
    list_filter = ('cohort',)
    fieldsets = (
        (None, {'fields': ('subject', 'teacher', 'is_active', )}),
    )
    pass


class GradeLevelAdmin(admin.ModelAdmin):
    ordering = ['order']
    pass


admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(SubjectCategory, SubjectCategoryAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(MarkingPeriod, MarkingPeriodAdmin)
admin.site.register(Cohort, CohortAdmin)
admin.site.register(EducativeProgram, EcucativeProgramAdmin)
admin.site.register(SchoolYear, SchoolYearAdmin)
admin.site.register(GradeLevel, GradeLevelAdmin)
admin.site.register(CourseEnrollment, CourseEnrollmentAdmin)
