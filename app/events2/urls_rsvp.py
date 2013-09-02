from django.conf.urls.defaults import *
from django.views.generic.base import TemplateView


urlpatterns = patterns('events.views',
	url(r'^$', 
        view='rsvp_list', 
        name='rsvp-list'
    ),
    # url(r'^/print/$', 
    #     view='rsvp_print', 
    #     name='rsvp-print'
    # ),
)
