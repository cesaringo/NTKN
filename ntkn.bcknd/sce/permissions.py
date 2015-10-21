from rest_framework import permissions
from .models import Student

class CanSeeCourseEnrollment(permissions.BasePermission):
	"""
	Permite que solo los estudiantes puedan ver solo sus propios course enrollments
	"""
	def has_object_permission(self, request, view, obj):
		student = Student.objects.get(username=request.user.username)
		if student is None:
			return false
		return obj.student == student
