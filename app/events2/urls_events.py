from django.conf.urls.defaults import *
from django.views.generic.base import TemplateView


urlpatterns = patterns('events.views',
	url(r'^$', 
        view='event_list', 
        name='event-list'
    ),
    url(r'^(?P<event_slug>[-\w]+)/$',
        view='event_list',
        name='event-detail'
    ),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$',
        view='event_list',
        name='event-month'
    ),
	url(r'^print/(?P<occurrence_id>\d+)/?$', 
        view='occurrence_print', 
        name='occurrence_print'
    ),

)
