from rest_framework import viewsets
from .serializers import StudentSerializer, CourseSerializer
from .models import Student, Course

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
	queryset = Course.objects.all()
	serializer_class = CourseSerializer