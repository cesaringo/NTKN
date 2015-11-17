from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from sce.serializers import (CourseSerializer, CourseEnrollmentSerializer,
							 SchoolYearSerializer, ScoreSerializer, SubjectSerializer)
from alumni.serializers import StudentSerializer
from sce.models import Course, CourseEnrollment, SchoolYear, Score, Subject
from alumni.models import Student, EducativeProgram
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.fields import empty
from rest_framework_bulk import BulkModelViewSet
from rest_framework.decorators import detail_route


class StudentViewSet(viewsets.ModelViewSet):
	"""	A viewset for viewing and editing Student instances. """
	serializer_class = StudentSerializer
	queryset = Student.objects.all()
	lookup_field = 'username'


class CourseViewSet(BulkModelViewSet):
	""" An API endpoint for the Course model """
	# permission_classes = (IsAdminUser,)
	# queryset = Course.objects.filter(is_active=True)
	serializer_class = CourseSerializer
	permission_classes = [IsAuthenticated, DjangoModelPermissions]
	queryset = Course.objects.none()  # Required for DjangoModelPermissions

	def get_queryset(self):
		user = self.request.user
		queryset = Course.objects.all()

		# if request by teacher
		if user.groups.all().filter(name='teacher').exists():
			queryset = queryset.filter(teacher=user)

		# if request by student
		elif user.groups.all().filter(name='student').exists():
			id_courses = CourseEnrollment.objects.filter(
				student__username=user.username).values_list('course_id', flat=True)
			queryset = queryset.filter(id__in=id_courses)

		# if requested by admin
		elif user.groups.all().filter(name='administrator').exist():
			# All courses
			pass
		else:
			queryset = None

		return queryset


class CourseEnrollmentViewSet(viewsets.ModelViewSet):
	"""	And API endpoint for CourseEnrollment model	"""
	serializer_class = CourseEnrollmentSerializer
	permission_classes = [IsAuthenticated, DjangoModelPermissions]
	queryset = CourseEnrollment.objects.none()  # Required for DjangoModelPermissions

	def get_queryset(self):
		queryset = CourseEnrollment.objects.all()
		user = self.request.user

		# if user:
		# 	student = Student.objects.filter(username = self.request.user.username)
		# 	if Student is None:
		# 		queryset = None
		# 	queryset = queryset.filter(student=student)

		return queryset

	# def list(self, request, *args, **kwargs):
	# 	if request.GET.get('fields'):
	# 		#self.get_serializer().fields = ('id',)
	# 		print(self.get_serializer().fields)

	# 	return super(CourseEnrollmentViewSet, self).list(request, *args, **kwargs)


	# def retrieve(self, request, *args, **kwargs):
	# 	if request.GET.get('fields'):
	# 		#self.get_serializer().fields = ('id',)
	# 		print(request.GET.get('fields'))

	# 	return super(CourseEnrollmentViewSet, self).list(request, *args, **kwargs)

	# from rest_framework.fields import empty
	# def get_serializer(self, instance=None, data=empty, many=False, partial=False):
	# 	fields = self.request.GET.get('fields', None)
	# 	if fields is not None:
	# 		fields = fields.split(',')


	# return CourseEnrollmentSerializer(instance=instance, data=data, many=many, partial=partial, fields=fields)


class SchoolYearViewSet(viewsets.ModelViewSet):
	serializer_class = SchoolYearSerializer
	queryset = SchoolYear.objects.all()
	permission_classes = [IsAuthenticated, DjangoModelPermissions]

	@detail_route()
	def create_registers(self, request, pk):
		"""
		:param request: querystring params (id_educative_program)
		:param pk: pk of the school year
		:return: error is some was wrong, result if success
		"""
		data = {}
		try:
			sy = SchoolYear.objects.get(pk=pk)
		except SchoolYear.DoesNotExist:
			sy = None

		if sy is None:
			data['has_error'] = True
			data['error_message'] = 'School year not found.'
			return Response(data=data, status=status.HTTP_404_NOT_FOUND)

		id_educative_program = request.GET.get('educative_program', None)
		if id_educative_program is None:
			data['has_error'] = True
			data['error_message'] = 'Educative program is required.'
			return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

		try:
			educative_program = EducativeProgram.objects.get(id=id_educative_program)
		except EducativeProgram.DoesNotExist:
			data['has_error'] = True
			data['error_message'] = 'Educative program does not exist.'
			return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

		data['courses'] = []
		subjects = educative_program.subject_set.all()
		for subject in subjects:
			for cohort in subject.cohorts.all():
				course = Course(
					school_year=sy,
					subject=subject,
					cohort=cohort
				)
				course.save()
				data['courses'].append({
					'id': course.id,
					'course': course.subject.fullname,
					'cohort': course.cohort.id
				})

		data['success'] = True
		data['success_message'] = 'Course added correctly.'
		return Response(data=data, status=status.HTTP_200_OK)


class ScoreViewSet(viewsets.ModelViewSet):
	serializer_class = ScoreSerializer
	queryset = Score.objects.all()


class SubjectViewSet(viewsets.ModelViewSet):
	serializer_class = SubjectSerializer
	queryset = Subject.objects.none()

	def get_queryset(self):
		# Filters
		query_string = self.request.GET
		queryset = Subject.objects.all()

		# hide inactive data if is not requested
		if 'include_inactive' in query_string:
			if query_string['include_inactive'] == 'true' or query_string['include_inactive'] == 1:
				pass
			else:
				queryset = queryset.filter(is_active=True)
		else:
			queryset = queryset.filter(is_active=True)

		# Find patters in fullname
		if 'search' in query_string:
			queryset = queryset.filter(fullname__icontains=query_string['search'])

		if 'educative_program' in query_string:
			queryset = queryset.filter(grade_level__educative_program__name__iexact=query_string['educative_program'])

		# End Filters
		return queryset

	def get_serializer(self, instance=None, data=empty, many=False, partial=False):
		fields = self.request.GET.get('fields', None)
		if fields is not None:
			fields = fields.split(',')
		return SubjectSerializer(instance=instance, data=data, many=many, partial=partial, fields=fields)
