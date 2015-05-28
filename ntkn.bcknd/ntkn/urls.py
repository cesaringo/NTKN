from django.conf.urls import patterns, include, url
from django.contrib import admin
from front.views import Home

urlpatterns = patterns('',
    # Examples:
    

    #url(r'^auth/', include('authentication.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^rest-auth/', include('rest_auth.urls')),
    #url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^.*$', Home.as_view(), name='home'),
    #url(r'^app/.*$', Home2.as_view(), name='home2'),
)
