from rest_framework import serializers
from alumni.models import Institute, GradeLevel, Student, Cohort
#from sce.serializers import SubjectSerializer


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


class GradeLevelSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = GradeLevel
        fields = ['id', 'name', 'slug', 'educative_program', 'order']


class IntituteSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Institute


class CohortSerializer(serializers.ModelSerializer):
	class Meta:
		model = Cohort
		fields = ['id', 'name']


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
