from django.conf.urls import patterns, include, url
from django.contrib import admin
from front.views import Home

urlpatterns = patterns('',
    # Examples:
    url(r'^$', Home.as_view(), name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^auth/', include('authentication.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
