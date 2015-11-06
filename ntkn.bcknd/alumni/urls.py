from alumni.views import (InstituteViewSet, StudentViewSet)
from rest_framework.routers import DefaultRouter
from django.conf.urls import patterns, url

router = DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'institutes', InstituteViewSet)

urlpatterns = router.urls
