import rest_framework
from rest_framework import serializers
from .models import (Student, Course, MarkingPeriod, Subject, 
	CourseEnrollment, Score, SchoolYear, GradeLevel, Cohort)


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
	"""
	A ModelSerializer that takes an additional 'fields' argument that
	controls which fields should be displayed.
	"""
	def __init__(self, *args, **kwargs):
		# Don't pass the 'fields' arg up to the superclass
		fields = kwargs.pop('fields', None)

		# Instantiate the superclass normally
		super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

		if fields is not None:
			# Drop any fields that are not specified in the `fields` argument.
			allowed = set(fields)
			existing = set(self.fields.keys())
			for field_name in existing - allowed:
				self.fields.pop(field_name)


class SchoolYearSerializer(serializers.ModelSerializer):
	class Meta:
		model = SchoolYear
		fields = ['id', 'name']


class GradeLevelSerializer(serializers.ModelSerializer):
	class Meta:
		model=GradeLevel

class CohortSerializer(serializers.ModelSerializer):
	class Meta:
		model=Cohort
		fields = ['id', 'name']


class MarkingPeriodSerializer(DynamicFieldsModelSerializer):
	"""
	Solo para consulta de los bimestres. No se pueden editar.
	"""
	id = serializers.IntegerField(read_only=True)
	name = serializers.CharField(read_only=True)
	shortname = serializers.CharField(read_only=True)

	class Meta:
		model = MarkingPeriod
		fields = ['id', 'name', 'shortname']
		ordering = ('name',)



class SubjectSerializer(serializers.ModelSerializer):
	class Meta:
		model = Subject


class StudentSerializer(DynamicFieldsModelSerializer):
	course_set = serializers.StringRelatedField(many=True)
	from rest_auth.serializers import PhotoSerializer
	photo = PhotoSerializer()
	year = GradeLevelSerializer()
	cohorts = CohortSerializer(many=True)

	class Meta:
		model = Student
		fields = ['id', 'first_name', 'last_name', 'sex', 'username', 'year', 'class_year', 'educative_program', 'course_set', 'photo', 'cohorts']
		depth = 1




class CourseSerializer(DynamicFieldsModelSerializer):
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
	id = serializers.IntegerField()
	marking_period = MarkingPeriodSerializer(read_only=True, fields=['id', 'name'])
	class Meta:
		model = Score
		fields = ('id', 'score', 'marking_period')


class CourseEnrollmentSerializer(DynamicFieldsModelSerializer):
	student = serializers.PrimaryKeyRelatedField(read_only=True)
	course = CourseSerializer(fields=['id','subject'], read_only=True)
	scores = ScoreSerializer(many=True)
	
	class Meta:
		model = CourseEnrollment
		#Default fields
		fields = ('id', 'student', 'course', 'is_active', 'scores', 'get_average')

	def update(self, instance, validated_data):
		# The unique field than can be edited in CourseEnrollment on list of Scores
		print(instance)
		for item in validated_data['scores']:
			score = Score.objects.get(pk=item['id'])
			score.score = item['score']
			score.save()
		instance.save()
		return instance

	






