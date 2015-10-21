from .views import (StudentViewSet, CourseViewSet,
	CourseEnrollmentViewSet, SchoolYearViewSet
	)
from rest_framework.routers import DefaultRouter
from django.conf.urls import patterns, url

router = DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'courses', CourseViewSet, base_name='Courses')
router.register(r'school-years', SchoolYearViewSet)
router.register(r'course-enrollments', CourseEnrollmentViewSet, base_name='CourseEnrollment')

urlpatterns = router.urls

urlpatterns += patterns('',
	#url(r'/hola^.*$', Home.as_view(), name='home'),
)
