from rest_framework import viewsets
from .serializers import (StudentSerializer, CourseSerializer, CourseEnrollmentSerializer, 
	SchoolYearSerializer, ScoreSerializer)
from .models import Student, Course, CourseEnrollment, SchoolYear, Score
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

		#Si la petición la hace un usuario con Rol de maestro				
		if user.groups.all().filter(name='teacher').exists():
			print('teacher')
			queryset = queryset.filter(teacher=user)

		#Si la petición la hace un usuario con Rol de estudiante	
		elif user.groups.all().filter(name='student').exists():
			print('student')
			id_courses = CourseEnrollment.objects.filter(
				student__username=user.username).values_list('course_id', flat=True)
			queryset = queryset.filter(id__in=id_courses)

		else:
			queryset=None
		
		return queryset

class CourseEnrollmentViewSet(viewsets.ModelViewSet):
	"""
	And API endpoint for CourseEnrollment model
	"""
	serializer_class = CourseEnrollmentSerializer
	permission_classes = [IsAuthenticated]


	def get_queryset(self):
		queryset = CourseEnrollment.objects.all()
		user = self.request.user

		# if user:
		# 	student = Student.objects.filter(username = self.request.user.username)
		# 	if Student is None:
		# 		queryset = None
		# 	queryset = queryset.filter(student=student)

		return queryset

	def list(self, request, *args, **kwargs):
		if request.GET.get('fields'):
			#self.get_serializer().fields = ('id',)
			print(self.get_serializer().fields)

		return super(CourseEnrollmentViewSet, self).list(request, *args, **kwargs)

		
		



class SchoolYearViewSet(viewsets.ModelViewSet):
	serializer_class = SchoolYearSerializer
	queryset = SchoolYear.objects.all()
	permission_classes = [IsAuthenticated,]

class ScoreViewSet(viewsets.ModelViewSet):
	serializer_class = ScoreSerializer
	queryset = Score.objects.all()
