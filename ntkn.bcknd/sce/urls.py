from .views import (StudentViewSet, CourseViewSet,
	CourseEnrollmentViewSet
	)
from rest_framework.routers import DefaultRouter
from django.conf.urls import patterns, url

router = DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'course-enrollments', CourseEnrollmentViewSet)

urlpatterns = router.urls

urlpatterns += patterns('',
	#url(r'/hola^.*$', Home.as_view(), name='home'),
)
