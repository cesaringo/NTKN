from rest_framework import viewsets
from .serializers import StudentSerializer, CourseSerializer, CourseEnrollmentSerializer
from .models import Student, Course, CourseEnrollment

class StudentViewSet(viewsets.ModelViewSet):
	"""
	A viewset for viewing and editing Student instances.
	"""
	serializer_class = StudentSerializer
	queryset = Student.objects.all()


class CourseViewSet(viewsets.ModelViewSet):
	"""
	an API endpoint for the Course model
	"""
	#permission_classes = (IsAdminUser,)
	queryset = Course.objects.filter(is_active=True)
	serializer_class = CourseSerializer

class CourseEnrollmentViewSet(viewsets.ModelViewSet):
	"""
	And API endpoint for CourseEnrollment model
	"""
	queryset = CourseEnrollment.objects.all()
	serializer_class = CourseEnrollmentSerializer
