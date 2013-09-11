from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()

# Configure dajaxice
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()

# Remove "Sites" from admin
from django.contrib.sites.models import Site
# admin.site.unregister(Site)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'app.views.home', name='home'),

    url(r'^$', include('app.main.urls')),
    url(r'^merit/', include('app.merit.urls')),

    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^pages', include('django.contrib.flatpages.urls')),


    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),


    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)
