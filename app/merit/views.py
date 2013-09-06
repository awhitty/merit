import datetime

from django.utils import simplejson
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from app.main.decorators import render_to

from events.models import Occurrence, RSVP
from announcements.models import Announcement

@render_to('merit/index.html')
def index(request):
    announcement_list = Announcement.objects.all().order_by('-published')

    paginator = Paginator(announcement_list, 5)

    page = request.GET.get('page')
    try:
        announcements = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        announcements = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        announcements = paginator.page(paginator.num_pages)

    return {'announcements': announcements}

@render_to('merit/occurrences.html')
def occurrences(request):
	occurrence_list = Occurrence.objects.public().filter(start_time__gt=datetime.datetime.now()).order_by('start_time')

	paginator = Paginator(occurrence_list, 25)

	page = request.GET.get('page')
	try:
		occurrences = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		occurrences = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		occurrences = paginator.page(paginator.num_pages)

	return {'occurrences': occurrences}

@render_to('merit/occurrence.html')
def occurrence(request, id):
	occurrence_item = Occurrence.objects.get(pk=id)
	previous_page = request.META.get('HTTP_REFERER', None)
	return {
		'occurrence': occurrence_item,
		'previous': previous_page
	}

@render_to('merit/rsvps.html')
def rsvps(request):
    rsvp_list = RSVP.objects.filter(user=request.user).order_by('occurrence__start_time')
    simple_stats = []
    total_duration = 0

    for rsvp in rsvp_list:
    	key = rsvp.occurrence.title

    	total_duration += rsvp.duration.total_seconds()

    	simple_stats.append({
    		'title': key,
    		'verified': rsvp.verified,
    		'timestamp': rsvp.occurrence.start_time.isoformat(),
    		'duration': rsvp.duration.total_seconds(),
    		'total_duration': total_duration
    	})

    simple_stats = simplejson.dumps(simple_stats)

    return {
    	'rsvps': rsvp_list,
    	'stats': simple_stats
    }

@render_to('merit/stats.html')
def stats(request):
    pass

# change password
# flat pages
# announcements?
# 