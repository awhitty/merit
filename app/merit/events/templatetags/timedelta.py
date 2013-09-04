import datetime

from django import template
from django.utils.timesince import timesince

register = template.Library()

def timedelta(value):
    if not value:
        return ''

	cmp = datetime.datetime.now()

	print "%s" % timesince(cmp,value)
	return "%s" % timesince(cmp,value)

register.filter('timedelta',timedelta)