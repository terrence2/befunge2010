from django.conf.urls.defaults import *

urlpatterns = patterns('puzzles.views',
	(r'^$', 'index'),
	(r'^shell/$', 'shell'),
	(r'^play/(?P<puzzle_id>\d+)/$', 'play'),
)

