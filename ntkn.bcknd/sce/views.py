from datetime import datetime

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from sce.serializers import (CourseSerializer, CourseEnrollmentSerializer,
	SchoolYearSerializer, ScoreSerializer, SubjectSerializer, StudentSerializer,
	InstituteSerializer, EducativeProgramSerializer)

from sce.models import (Course, CourseEnrollment, SchoolYear, Score, Subject, Student, Institute,
						EducativeProgram)

from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.fields import empty
from rest_framework_bulk import BulkModelViewSet
from rest_framework.decorators import detail_route
import re


class InstituteViewSet(viewsets.ModelViewSet):
	serializer_class = InstituteSerializer
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
		print (user.groups.all())

		# if request by teacher
		if user.groups.all().filter(name='teacher').exists():
			queryset = queryset.filter(teacher=user)

		# if request by student
		elif user.groups.all().filter(name='student').exists():
			id_courses = CourseEnrollment.objects.filter(
				student__username=user.username).values_list('course_id', flat=True)
			queryset = queryset.filter(id__in=id_courses)

		# if requested by admin
		elif user.groups.all().filter(name='administrator').exists():
			# All courses
			pass
		else:
			queryset = Course.objects.none()

		return queryset

	@detail_route(methods=['post'])
	def enroll_students(self, request, pk):
		try:
			course = Course.objects.get(pk=pk)
		except Course.DoesNotExist:
			course = None

		if course is None:
			return Response(data={
				'has_error': True,
				'error_message': 'Course with pk = {0} does not exists.'.format(pk)
			}, status=status.HTTP_400_BAD_REQUEST)

		id_students = request.GET.get('id_students', None)
		if id_students is None:
			return Response(data={
				'has_error': True,
				'error_message': 'param id_students is required'
			}, status=status.HTTP_400_BAD_REQUEST)

		pattern = re.compile("^(\d+(,\d+)*)?$")
		if not pattern.match(id_students):
			return Response(data={
				'has_error': True,
				'error_message': 'id_students is not a valid param. Please use coma separated ints.'
			}, status=status.HTTP_400_BAD_REQUEST)

		id_students = id_students.split(',')
		students = Student.objects.filter(id__in=id_students)
		course_enrollments = []
		for student in students:
			course_enrollment = CourseEnrollment(student=student, course=course)
			try:
				course_enrollment.save()
				course_enrollments.append(course_enrollment)
			except:
				# If a Course enrollment for the given student and course already exist.
				pass

		course_enrollment_serializer = CourseEnrollmentSerializer(course_enrollments, many=True)
		return Response(
			data={
				'success': True,
				'result': course_enrollment_serializer.data
			}, status=status.HTTP_200_OK
		)


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

	@detail_route(methods=['post'])
	def create_courses(self, request, pk):
		try:
			sy = SchoolYear.objects.get(pk=pk)
		except SchoolYear.DoesNotExist:
			sy = None

		if sy is None:
			return Response(data={
				'has_error': True,
				'error_message': 'School year not found.'
			}, status=status.HTTP_404_NOT_FOUND)

		current_courses = Course.objects.filter(school_year=sy)
		exist_courses = current_courses.exists()
		complete_courses = request.DATA.get('complete_courses', False)

		if exist_courses and not complete_courses:
			return Response(data={
				'has_error': True,
				'error_message': 'There is already courses for the given period. Use complete_courses option.'
			}, status=status.HTTP_400_BAD_REQUEST)

		courses = []
		subjects = sy.educative_program.get_subjects()
		for subject in subjects:
			for cohort in subject.grade_level._get_cohorts():
				if current_courses.filter(subject=subject, cohort=cohort).exists():
					continue # Only unique courses
				course = Course(
					school_year=sy,
					subject=subject,
					cohort=cohort
				)
				courses.append(course)

		Course.objects.bulk_create(courses)
		course_serializer = CourseSerializer(data=courses, many=True, fields=['subject', 'school_year', 'cohort'])
		course_serializer.is_valid()
		return Response(data={
			'success': True,
			'success_message': 'Course added correctly.',
			'created_courses': course_serializer.data
		},status=status.HTTP_200_OK)

	@detail_route(methods=['post'])
	def activate(self, request, pk):
		try:
			sy = SchoolYear.objects.get(pk=pk)
		except SchoolYear.DoesNotExist:
			sy = None

		if sy is None:
			return Response(data={
				'has_error': True,
				'error_message': 'Periodo escolar con el id: {0} no existe'.format(pk)
			}, status=status.HTTP_400_BAD_REQUEST)

		sy.is_active = True
		sy.save()
		return Response(data={
			'success': True,
			'success_message': 'Periodo escolar con el id: {0} activado correctamente'.format(pk),
			'result': SchoolYearSerializer(sy, fields=['id', 'slug', 'is_active', 'start_date',
													   'end_date', 'educative_program__name']).data
			}, status=status.HTTP_200_OK)

	@detail_route(methods=['post'])
	def deactivate(self, request, pk):
		try:
			sy = SchoolYear.objects.get(pk=pk)
		except SchoolYear.DoesNotExist:
			sy = None

		if sy is None:
			return Response(data={
				'has_error': True,
				'error_message': 'Periodo escolar con el id: {0} no existe'.format(pk)
			}, status=status.HTTP_400_BAD_REQUEST)

		sy.is_active = False
		sy.save()
		return Response(data={
			'success': True,
			'success_message': 'Periodo escolar con el id: {0} desactivado correctamente'.format(pk),
			'result': SchoolYearSerializer(sy, fields=['id', 'slug', 'is_active', 'start_date',
													   'end_date', 'educative_program__name']).data
			}, status=status.HTTP_200_OK)


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
