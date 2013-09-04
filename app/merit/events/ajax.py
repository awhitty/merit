
from django.utils import simplejson
from django.template.loader import render_to_string

from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register

from models import Occurrence, RSVP

from utils import create_rsvp, destroy_rsvp

def refresh_button(request, occurrence):
	new_button = render_to_string('rsvp_button.html', {
		'request': request,
		'occurrence': occurrence
	})

	dajax = Dajax()
	dajax.add_data({
		'selector': '#rsvp-%s' % occurrence.id,
		'content': new_button
	}, 'replace_selector')

	return dajax.json()

@dajaxice_register(method='POST', name='events.add_rsvp')
def add_rsvp(request, occurrence_id):
	occurrence = Occurrence.objects.get(pk=occurrence_id)
	create_rsvp(request.user, occurrence)

	return refresh_button(request, occurrence)

@dajaxice_register(method='POST', name='events.delete_rsvp')
def delete_rsvp(request, rsvp_id):
	rsvp = RSVP.objects.get(pk=rsvp_id)
	occurrence = rsvp.occurrence

	destroy_rsvp(rsvp)

	return refresh_button(request, occurrence)