from django.conf.urls import patterns, include, url
from django.contrib import admin
from front.views import Home
from ntkn import settings
urlpatterns = patterns('',
    # Examples:
    

    #url(r'^auth/', include('authentication.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^rest-auth/', include('rest_auth.urls')),

    #SCE API
    url(r'^sce-api/', include('sce.urls')),
    #url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    
    #url(r'^app/.*$', Home2.as_view(), name='home2'),

)

if settings.DEBUG :
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )

urlpatterns += patterns('',
	url(r'^.*$', Home.as_view(), name='home'),
)