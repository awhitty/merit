import datetime

from django import template
from django.utils.timesince import timesince
from django.utils import timezone

register = template.Library()

@register.filter(name='timedelta')
def timedelta(value):
	if not value:
		return

	start = timezone.now()
	end = start + value

	return "%s" % timesince(start,end)