from rest_framework import serializers

from alumni.serializers import DynamicFieldsModelSerializer
from sce.models import (Course, MarkingPeriod, Subject,
	CourseEnrollment, Score, SchoolYear, GradeLevel, Cohort)


class SchoolYearSerializer(serializers.ModelSerializer):
	class Meta:
		model = SchoolYear
		fields = ['id', 'name']


class GradeLevelSerializer(serializers.ModelSerializer):
	class Meta:
		model=GradeLevel




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

class CourseSerializer(DynamicFieldsModelSerializer):
	marking_periods = serializers.SlugRelatedField(many=True, slug_field='shortname', read_only=True)
	subject = serializers.StringRelatedField()
	teacher = serializers.StringRelatedField()
	school_year = serializers.StringRelatedField()
	cohort = serializers.StringRelatedField()
	#alumni = StudentSerializer(many=True)#
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

	






