from django.conf import settings
from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

from puzzles.models import Puzzle
admin.site.register(Puzzle)

urlpatterns = patterns('',
    # Example:
    # (r'^webfunge/', include('webfunge.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^admin/', include(admin.site.urls)),
    (r'^puzzles/', include('puzzles.urls')),
)

if settings.DEBUG:
	urlpatterns += patterns('',
		(r'^media/(?P<path>.*)$', 'django.views.static.serve', 
			{'document_root': settings.MEDIA_ROOT}),
	)

