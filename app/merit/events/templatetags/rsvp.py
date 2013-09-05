
from django import template
from django.utils import timezone
from django.template.loader import render_to_string
from django.contrib.auth.models import User
# from django.utils.safestring import mark_safe

from ..models import EventType, Occurrence, RSVP

register = template.Library()

@register.simple_tag
def rsvp_button(req, occ, classes=None):
	rsvp_exists   = req.user in occ.users.all()
	rsvp_required = occ.required
	rsvp_past     = occ.start_time < timezone.now()
	rsvp_full     = occ.is_full

	status = 'add'

	if rsvp_exists:
		rsvp = RSVP.objects.get(occurrence=occ, user=req.user)

		if rsvp.verified:
			status = 'verified'
		elif rsvp_past:
			status = 'pending'
		elif rsvp_required:
			status = 'required'
		else:
			status = 'delete'

	elif rsvp_full:
		status = 'full'
		
	else:
		status = 'add'


	t =  'includes/rsvp_%s.html' % status

	if rsvp_exists and rsvp:
		c = {'rsvp': rsvp, 'classes': classes}
	else:
		c = {'occurrence': occ, 'classes': classes}

	return render_to_string(t, c)