from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.simple_tag
def navactive(request, urls):
	if request.path in ( reverse(url) for url in urls.split() ):
		return "active"
	return ""

@register.simple_tag
def flatpageactive(request, url):
	if request.path == reverse('django.contrib.flatpages.views.flatpage', kwargs={'url':url}):
		return "active"

	return ""