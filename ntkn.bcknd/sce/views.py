from rest_framework import viewsets
from .serializers import StudentSerializer, CourseSerializer, CourseEnrollmentSerializer, SchoolYearSerializer
from .models import Student, Course, CourseEnrollment, SchoolYear
from rest_framework.permissions import IsAuthenticated
from .permissions import CanSeeCourseEnrollment

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
	#queryset = Course.objects.filter(is_active=True)
	serializer_class = CourseSerializer
	permission_classes = [IsAuthenticated,]

	def get_queryset(self):
		user = self.request.user
		queryset = Course.objects.all()

		
		if user.groups.all().filter(name='teacher').exists():
			queryset = queryset.filter(teacher=user)

		else:
			queryset=None
		
		return queryset

class CourseEnrollmentViewSet(viewsets.ModelViewSet):
	"""
	And API endpoint for CourseEnrollment model
	"""
	serializer_class = CourseEnrollmentSerializer
	#permission_classes = [IsAuthenticated, CanSeeCourseEnrollment]

	def get_queryset(self):
		queryset = CourseEnrollment.objects.all()
		user = self.request.user

		# if user:
		# 	student = Student.objects.filter(username = self.request.user.username)
		# 	if Student is None:
		# 		queryset = None
		# 	queryset = queryset.filter(student=student)

		return queryset

class SchoolYearViewSet(viewsets.ModelViewSet):
	serializer_class = SchoolYearSerializer
	queryset = SchoolYear.objects.all()
	permission_classes = [IsAuthenticated,]

