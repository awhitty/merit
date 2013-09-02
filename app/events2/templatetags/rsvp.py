import datetime

from django import template
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

from events.models import EventType, Occurrence, RSVP, CustomUser
from events.helpers import add_rsvp

register = template.Library()

@register.simple_tag
def rsvp_button(request, occurrence):
	c_user = CustomUser.objects.get(username=request.user.username)
	# try:
	# 	occurrence = Occurrence.objects.get(pk=occurrence_id)
	# except:
	# 	return "No occurrence with id %s" % (occurrence_id)

	rsvp_exists = c_user in occurrence.users.all()
	full        = occurrence.event.capacity and occurrence.users.all().count() >= occurrence.event.capacity
	passed      = occurrence.passed
	required    = occurrence.event.required
	if rsvp_exists:
		rsvp = RSVP.objects.get(user=c_user, occurrence=occurrence)
		verified    = rsvp_exists and rsvp.verified
		pending 	= rsvp_exists and passed
	response = ""

	if rsvp_exists:
		if verified:
			response = mark_safe('<button class="btn btn-success disabled" data-id="%s" data-action="none" rel="tooltip" title="Verified on %s" data-placement="right"><i class="icon-check"></i> Verified</a>' % (occurrence.pk, rsvp.verified_date.strftime('%x')))
		elif pending:
			response = mark_safe('<button class="btn btn-info disabled" data-id="%s" data-action="none"><i class="icon-check-empty"></i> Pending</a>' % (occurrence.pk))
		elif required:
			response = mark_safe('<button class="btn disabled" data-action="none"><i class="icon-minus"></i> RSVP</a>')
		else:
			response = mark_safe('<button class="btn btn-rsvp btn-danger" data-id="%s" data-action="delete"><i class="icon-minus"></i> RSVP</a>' % (occurrence.pk))
	elif not passed:
		if required:
			add_rsvp(request, occurrence)
			return rsvp_button(request, occurrence_id)
		elif not full:
			response = mark_safe('<button class="btn btn-primary btn-rsvp" data-id="%s" data-action="add"><i class="icon-plus"></i> RSVP</a>' % (occurrence.pk))
		else:
			response = mark_safe('<button class="btn disabled" data-action="none"><i class="icon-plus"></i> RSVP</a>')
	else:
		response = mark_safe('<button class="btn disabled" data-action="none"><i class="icon-warning-sign"></i> Passed</a>')

	return response

@register.filter
def get_hours(request, event_type):
	"""Gets the specified user's hours and returns a timedelta object."""
	if event_type.is_total:
		duration = datetime.timedelta(0)
		et_set = EventType.objects.all().exclude(title=event_type.title)
		for et in et_set:
			duration += get_hours(request, et)
	else:
		if isinstance(request, User):
			user = request
		else:
			user = request.user

		rset = RSVP.objects.filter(user=user, occurrence__event__event_type=event_type, verified=True)
		duration = datetime.timedelta(0)
		for rsvp in rset:
			duration += rsvp.duration
	return duration

@register.filter
def get_hours_as_percent(request, event_type):
	"""Gets the specified user's hours and returns a timedelta object."""
	if isinstance(request, User):
		user = request
	else:
		user = request.user
	rset = RSVP.objects.filter(user=user, occurrence__event__event_type=event_type)
	duration = get_hours(request, event_type)

	d_seconds = duration.total_seconds()
	et_seconds = event_type.quota.total_seconds()

	return d_seconds/et_seconds*100

# <a href="#" class="btn btn-primary"><i class="icon-plus"></i> RSVP</a>