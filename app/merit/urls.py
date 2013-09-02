from django.conf.urls import patterns, url


urlpatterns = patterns('app.merit.views',
    url(r'^$', 'index', name='merit-home'),
    url(r'^occurrences/$', 'occurrences', name='merit-occurrences'),
    url(r'^occurrence/$', 'occurrence', name='merit-occurrence'),
    url(r'^rsvps/$', 'rsvps', name='merit-rsvps'),
    url(r'^stats/$', 'stats', name='merit-stats'),
)
