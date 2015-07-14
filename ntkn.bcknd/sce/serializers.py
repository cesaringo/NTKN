import rest_framework
from rest_framework import serializers
from .models import Student, Course

class StudentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Student
		fields = ['first_name', 'mname', 'last_name', 'sex', 'year', 'class_year']
	
class CourseSerializer(serializers.ModelSerializer):

	class Meta: 
		model = Course