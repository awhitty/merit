import datetime

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from app.main.decorators import render_to

from events.models import *

@render_to('merit/index.html')
def index(request):
    pass

@render_to('merit/occurrences.html')
def occurrences(request):
	occurrence_list = Occurrence.objects.public().filter(start_time__gt=datetime.datetime.now())

	paginator = Paginator(occurrence_list, 50)

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
    pass

@render_to('merit/stats.html')
def stats(request):
    pass

# change password
# flat pages
# announcements?
# 