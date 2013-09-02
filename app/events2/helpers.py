import sys
from django.contrib import messages

from events.models import RSVP, CustomUser

def add_rsvp(request, occurrence):
  try:
    if occurrence.event.capacity and occurrence.users.count() >= occurrence.event.capacity:
      messages.error(request, 'This event is full.')
      return False
    elif request.user in occurrence.users.all():
    	messages.warning(request, 'You have already RSVP\'d for this event.')
    	return True
    else:
      create_rsvp(request.user, occurrence)
      messages.success(request, 'Your RSVP to %s was successfully added.' % (occurrence.title))
      return True
  except :
    messages.error(request, 'Your RSVP could not be added.')
    return False

def remove_rsvp(request, rsvp):
	try:
		if rsvp.occurrence.event.required:
			messages.error(request, 'This event is required.')
			return False
		else:
			rsvp.delete()
			messages.success(request, 'Your RSVP to %s was successfully removed.' % (rsvp.title))
			return True
	except:
		messages.error(request, 'Your RSVP could not be removed.')
		return False

def create_rsvp(user, occurrence):
  try:
    custom_user = CustomUser.objects.get(username=user.username)
    print custom_user
    rs = RSVP(user=custom_user, occurrence=occurrence)
    rs.save()
    return True
  except:
    print "Unexpected error:", sys.exc_info()[0]
    return False

def bulk_rsvp(users, occurrence):
  for user in users:
    create_rsvp(user, occurrence)
