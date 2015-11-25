from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

from alumni.serializers import IntituteSerializer, StudentSerializer
from sce.serializers import EducativeProgramSerializer
from alumni.models import Student, Institute
from sce.models import EducativeProgram

class InstituteViewSet(viewsets.ModelViewSet):
	serializer_class = IntituteSerializer
	queryset = Institute.objects.all()
	permission_classes = [IsAuthenticated]


class StudentViewSet(viewsets.ModelViewSet):
	"""
	A viewset for viewing and editing Student instances.
	"""
	serializer_class = StudentSerializer
	queryset = Student.objects.none()
	lookup_field = 'username'
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		queryset = Student.objects.all()
		user = self.request.user

		# if resource is requested by teacher
		if user.groups.all().filter(name='teacher').exists():
			# Only Students on his courses
			pass

		# if resource is requested by student
		elif user.groups.all().filter(name='student').exists():
			queryset = queryset.filter(username=user.username)

		return queryset


class EducativeProgramViewSet(viewsets.ModelViewSet):
	serializer_class = EducativeProgramSerializer
	queryset = EducativeProgram.objects.all()
	permission_classes = [IsAuthenticated]