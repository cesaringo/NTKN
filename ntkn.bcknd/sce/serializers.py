from rest_framework import serializers
from alumni.serializers import DynamicFieldsModelSerializer
from sce.models import *
from sce.validators import validate_id_exists
from rest_framework_bulk import BulkListSerializer, BulkSerializerMixin


class IntituteSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Institute


class EducativeProgramSerializer(DynamicFieldsModelSerializer):
    subject_set = SubjectSerializer(many=True, read_only=True)
    class Meta:
        model = EducativeProgram
        fields = ['id', 'name', 'slug', 'num_of_levels', 'institute', 'is_active',
                  'subject_set', 'markingperiod_set']
        depth = 1


class GradeLevelSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = GradeLevel
        fields = ['id', 'name', 'slug', 'educative_program', 'order']


class StudentSerializer(DynamicFieldsModelSerializer):
    course_set = serializers.StringRelatedField(many=True)
    from rest_auth.serializers import PhotoSerializer
    photo = PhotoSerializer()
    grade_level = GradeLevelSerializer()
    cohorts = CohortSerializer(many=True)

    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'sex', 'username', 'grade_level', 'course_set', 'photo', 'cohorts']
        depth = 1


class CohortSerializer(serializers.ModelSerializer):
	class Meta:
		model = Cohort
		fields = ['id', 'name']


class SchoolYearSerializer(DynamicFieldsModelSerializer):
	educative_program_id = serializers.IntegerField(write_only=True)
	class Meta:
		model = SchoolYear
		fields = ('id', 'slug', 'start_date', 'end_date', 'is_active', 'educative_program', 'educative_program_id', 'num_of_courses')
		depth = 1


class GradeLevelSerializer(serializers.ModelSerializer):
	class Meta:
		model = GradeLevel
		depth = 1


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
		fields = ['id', 'name', 'shortname', 'grades_due']
		ordering = ('name',)


class SubjectSerializer(DynamicFieldsModelSerializer):
	class Meta:
		model = Subject
		fields = ('id', 'is_active', 'name', 'code', 'graded', 'description', 'level', 'order',
				  'grade_level', 'department', 'category')


class CourseSerializer(BulkSerializerMixin, DynamicFieldsModelSerializer):
	marking_periods = serializers.SlugRelatedField(many=True, slug_field='shortname', read_only=True)
	subject = serializers.StringRelatedField(read_only=True, allow_null=True)
	subject_id = serializers.IntegerField(write_only=True, validators=[validate_id_exists(Subject)])

	teacher = serializers.StringRelatedField(read_only=True)
	teacher_id = serializers.IntegerField(write_only=True, required=False, validators=[validate_id_exists(Teacher)])

	school_year = SchoolYearSerializer(read_only=True)
	school_year_id = serializers.IntegerField(write_only=True, validators=[validate_id_exists(SchoolYear)])

	cohort = serializers.StringRelatedField(read_only=True)
	cohort_id = serializers.IntegerField(write_only=True, validators=[validate_id_exists(Cohort)])

	students = serializers.StringRelatedField(many=True, required=False)

	class Meta:
		model = Course
		fields = ['id',
				  'subject',
				  'subject_id',
				  'teacher',
				  'teacher_id',
				  'school_year',
				  'school_year_id',
				  'cohort',
				  'cohort_id',
				  'marking_periods',
				  'students']

		#depth = 1
		list_serializer_class = BulkListSerializer

	def create(self, validated_data):
		print('Saving...')
		if 'students' in validated_data:
			students_data = validated_data.pop('students')
		course = Course.objects.create(**validated_data)
		return  course


	def validate(self, attrs):
		print('Validating data...')
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


