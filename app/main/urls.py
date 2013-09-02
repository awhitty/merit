from django.conf.urls import patterns, include, url


urlpatterns = patterns('app.main.views',
    url(r'^$', 'index', name='home'),
)
