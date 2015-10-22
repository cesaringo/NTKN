import rest_framework
from rest_framework import serializers
from .models import (Student, Course, MarkingPeriod, Subject, 
	CourseEnrollment, Score, SchoolYear, GradeLevel, Cohort)



class MarkingPeriodSerializer(serializers.ModelSerializer):
	class Meta:
		model = MarkingPeriod
		fields = ['name', 'shortname']
		ordering = ('name',)

class SubjectSerializer(serializers.ModelSerializer):
	class Meta:
		model = Subject

class CourseSerializer(serializers.ModelSerializer):

	def __init__(self, *args, **kwargs):
		fields = kwargs.pop('fields', None)
		super(CourseSerializer, self).__init__(*args, **kwargs)

		if fields is not None:
			allowed = set(fields)
			existing = set(self.fields.keys())
			for field_name in existing - allowed:
				self.fields.pop(field_name)

	#marking_periods = MarkingPeriodSerializer(many=True)
	marking_periods = serializers.SlugRelatedField(many=True, slug_field='shortname', read_only=True)
	subject = serializers.StringRelatedField()
	teacher = serializers.StringRelatedField()
	school_year = serializers.StringRelatedField()
	cohort = serializers.StringRelatedField()
	#students = StudentSerializer(many=True)#
	students = serializers.StringRelatedField(many=True)

	class Meta: 
		model = Course
		fields = ['id', 'subject', 'teacher', 'school_year', 'cohort', 'marking_periods', 'students']



class ScoreSerializer(serializers.ModelSerializer):
	class Meta:
		model = Score
		fields = ['score', 'marking_period']
		depth = 1


class CourseEnrollmentSerializer(serializers.ModelSerializer):
	scores = ScoreSerializer(many=True)
	#course = CourseSerializer()
	class Meta:
		model = CourseEnrollment
		fields = ['id', 'student', 'course', 'is_active', 'scores', 'get_avarage']


class GradeLevelSerializer(serializers.ModelSerializer):
	class Meta:
		model=GradeLevel

class CohortSerializer(serializers.ModelSerializer):
	class Meta:
		model=Cohort
		fields = ['id', 'name']

class StudentSerializer(serializers.ModelSerializer):
	course_set = serializers.StringRelatedField(many=True)
	from rest_auth.serializers import PhotoSerializer
	photo = PhotoSerializer()
	year = GradeLevelSerializer()
	cohorts = CohortSerializer(many=True)
	class Meta:
		model = Student
		fields = ['first_name', 'last_name', 'sex', 'username', 'year', 'class_year', 'educative_program', 'course_set', 'photo', 'cohorts']
		depth = 1

class SchoolYearSerializer(serializers.ModelSerializer):
	class Meta:
		model = SchoolYear
		fields = ['id', 'name']
