from django.conf.urls import patterns, url


urlpatterns = patterns('app.merit.views',
    url(r'^$', 'index', name='merit-home'),
    url(r'^occurrences/$', 'occurrences', name='merit-occurrences'),
    url(r'^occurrence/(?P<id>\d+)$', 'occurrence', name='merit-occurrence'),
    url(r'^rsvps/$', 'rsvps', name='merit-rsvps'),
    url(r'^stats/$', 'stats', name='merit-stats'),
)

# accounts stuff... not totally sure where to put this yet
urlpatterns += patterns('django.contrib.auth.views',
    url(r'^accounts/login/$', 'login', {'template_name': 'merit/login.html'}, name='merit-login'),
    url(r'^accounts/logout/$', 'logout', {'template_name': 'merit/logged_out.html'}, name='merit-logout'),
)
