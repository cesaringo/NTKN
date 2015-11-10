from rest_framework import serializers
from alumni.serializers import DynamicFieldsModelSerializer
from sce.models import (Course, MarkingPeriod, Subject,
						CourseEnrollment, Score, SchoolYear, GradeLevel, Cohort)
from alumni.models import Teacher
from sce.validators import validate_id_exists

class SchoolYearSerializer(DynamicFieldsModelSerializer):
	class Meta:
		model = SchoolYear
		fields = ('id', 'name', 'start_date', 'end_date', 'active_year')


class GradeLevelSerializer(serializers.ModelSerializer):
	class Meta:
		model = GradeLevel


class CohortSerializer(serializers.ModelSerializer):
	class Meta:
		model = Cohort
		fields = ['id', 'name']


class MarkingPeriodSerializer(DynamicFieldsModelSerializer):
	"""	Solo para consulta de los bimestres. No se pueden editar. """
	id = serializers.IntegerField(read_only=True)
	name = serializers.CharField(read_only=True)
	shortname = serializers.CharField(read_only=True)

	class Meta:
		model = MarkingPeriod
		fields = ['id', 'name', 'shortname']
		ordering = ('name',)


class SubjectSerializer(DynamicFieldsModelSerializer):
	class Meta:
		model = Subject
		fields = ('id', 'is_active', 'fullname', 'shortname', 'graded', 'description', 'level', 'order',
				  'grade_level', 'department', 'category')


class CourseSerializer(DynamicFieldsModelSerializer):
	marking_periods = serializers.SlugRelatedField(many=True, slug_field='shortname', read_only=True)
	subject = serializers.StringRelatedField(read_only=True)
	subject_id = serializers.IntegerField(write_only=True, validators=[validate_id_exists(Subject)])

	teacher = serializers.StringRelatedField(read_only=True)
	teacher_id = serializers.IntegerField(write_only=True, required=False, validators=[validate_id_exists(Teacher)])

	school_year = SchoolYearSerializer(read_only=True)
	school_year_id = serializers.IntegerField(write_only=True, validators=[validate_id_exists(SchoolYear)])

	cohort = serializers.StringRelatedField(read_only=True)
	cohort_id = serializers.IntegerField(write_only=True, validators=[validate_id_exists(Cohort)])

	students = serializers.StringRelatedField(many=True)

	class Meta:
		model = Course
		fields = ['id', 'subject', 'subject_id', 'teacher', 'teacher_id', 'school_year', 'school_year_id',
			'cohort', 'cohort_id', 'marking_periods', 'students']

		depth = 1

	def create(self, validated_data):
		students_data = validated_data.pop('students')
		course = Course.objects.create(**validated_data)
		for student in students_data:
			pass
		return course

	def validate(self, attrs):
		if Course.objects.filter(subject__id=attrs['subject_id'], school_year__id=attrs['school_year_id'],
			cohort__id=attrs['cohort_id']).exists():
			raise serializers.ValidationError('Course with given data already exists')
		return attrs


class ScoreSerializer(serializers.ModelSerializer):
	id = serializers.IntegerField()
	marking_period = MarkingPeriodSerializer(read_only=True, fields=['id', 'name'])

	class Meta:
		model = Score
		fields = ('id', 'score', 'marking_period')


class CourseEnrollmentSerializer(DynamicFieldsModelSerializer):
	student = serializers.PrimaryKeyRelatedField(read_only=True)
	course = CourseSerializer(fields=['id', 'subject'], read_only=True)
	scores = ScoreSerializer(many=True)

	class Meta:
		model = CourseEnrollment
		# Default fields
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
