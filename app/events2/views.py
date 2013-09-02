import datetime, calendar

from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from events.models import Occurrence, RSVP, EventType, Event

def event_list(request, event_slug=None, year=None, month=None):
	e = None
	if not event_slug is None:
		e = get_object_or_404(Event, slug=event_slug)
		dtstart = datetime.datetime.now()
		occurrences = Occurrence.public.filter(event__slug=event_slug, start_time__gt=datetime.datetime.now())
	elif year and month:
		occurrences = Occurrence.public.filter(start_time__year=year, start_time__month=month)
		d = year + "/"
		iyear, imonth = int(year), int(month)
		dtstart = datetime.datetime(iyear, imonth, 1)
	else:
		dtstart = datetime.datetime.now()
		occurrences = Occurrence.public.filter(start_time__gte=datetime.datetime.now())

	paginator = Paginator(occurrences, 40)
	page = request.GET.get('page')
	try:
		oc_page = paginator.page(page)
	except PageNotAnInteger:
		oc_page = paginator.page(1)
	except EmptyPage:
		oc_page = paginator.page(paginator.num_pages)


	last_day = calendar.monthrange(dtstart.year, dtstart.month)[1]
	response = {
		'request': request, 
		'occurrences': oc_page, 
		'event': e,
		'this_month' : dtstart,
		'next_month' : dtstart + datetime.timedelta(days=+last_day),
		'last_month' : dtstart + datetime.timedelta(days=-1),
	}
	# occurrences = Occurrence.objects.filter()

	return render_to_response('events/event_table.html', response)

def rsvp_list(request):

	# occurrences = Occurrence.objects.filter(start_time__gt=datetime.datetime.now())
	# TODO: add total hours?
	event_types = EventType.objects.all()
	if request.GET.get('print', False) == 'True':
		if request.GET.get('blank', False) == 'True':
			return render_to_response('events/blank_print.html', {'request':request})
		else:
			rsvps = RSVP.objects.all().filter(user = request.user).order_by('date').exclude(verified=True)
			template = 'events/rsvp_table_print.html'
	else:
		rsvps = RSVP.objects.all().filter(user = request.user).order_by('date')
		template = 'events/rsvp_table.html'
	return render_to_response(template, { 'request': request, 'rsvps': rsvps, 'event_types': event_types })

def occurrence_print(request, occurrence_id):
	occurrence = get_object_or_404(Occurrence, pk=occurrence_id)
	return render_to_response('events/occurrence_print.html', {'request': request, 'occurrence': occurrence})
