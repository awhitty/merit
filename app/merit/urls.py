from django.conf.urls import patterns, url, include


urlpatterns = patterns('app.merit.views',
    url(r'^$', 'index', name='merit-home'),
    url(r'^occurrences/$', 'occurrences', name='merit-occurrences'),
    url(r'^occurrence/(?P<id>\d+)/$', 'occurrence', name='merit-occurrence'),
    url(r'^occurrence/print/(?P<id>\d+)/$', 'occurrence_print', name='merit-print'),
    url(r'^rsvps/$', 'rsvps', name='merit-rsvps'),
    url(r'^rsvps/blank$', 'blank_sheet', name='merit-blank-sheet'),
    url(r'^stats/$', 'stats', name='merit-stats'),
)

# accounts stuff... not totally sure where to put this yet
urlpatterns += patterns('django.contrib.auth.views',
    url(r'^accounts/login/$', 'login', {'template_name': 'merit/login.html'}, name='merit-login'),
    url(r'^accounts/logout/$', 'logout', {'template_name': 'merit/logged_out.html'}, name='merit-logout'),
    url(r'^accounts/edit/password/$', 'password_change', {'template_name': 'merit/change_password.html'}, name='merit-change-password'),
    url(r'^accounts/edit/password/done/$', 'password_change_done', {'template_name': 'merit/change_password_done.html'}, name='merit-change-password-done'),
)