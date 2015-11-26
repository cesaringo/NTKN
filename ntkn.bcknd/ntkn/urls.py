from django.conf.urls import patterns, include, url
from django.contrib import admin
from front.views import Home
from ntkn import settings

urlpatterns = patterns('',
    # Admin
    url(r'^admin/', include(admin.site.urls)),

    # API | BackEnd
    url(r'^api/auth/', include('rest_auth.urls')),
    url(r'^api/sce/', include('sce.urls')),

    # FrontEnd
    url(r'^.*$', Home.as_view(), name='home'),
)

if settings.DEBUG :
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )
