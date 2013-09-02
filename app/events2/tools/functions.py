# Functions for the sake of DRY
import random, string, datetime

from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404, HttpResponseRedirect

from events.models import RSVP, Occurrence


def do_create_rsvp(user, occurrence_id):
  try:
    oc = Occurrence.objects.get(pk=occurrence_id)
  except:
    return 'The occurrence could not be found with the given parameters.'
  try:
    code = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(8))
    rs = RSVP(user=user, occurrence=oc, verification_code=code,)
    rs.save()
    print '%s to %s' % (user.get_full_name(), oc.title)
  except:
    print 'Failed: %s to %s' % (user.get_full_name(), oc.title)
  
def do_bulk_rsvp(occurrence_id, group = "all"):
  """docstring for bulk_rsvp"""
  try:
    if group == "all":
      user_list = User.objects.all()
    else:
      group = Group.objects.get(pk=group)
      user_list = User.objects.filter(groups=group)
  except:
    return 'The user list could not be generated.'
  for user in user_list:
    do_create_rsvp(user, occurrence_id)
  return 'Done.'
  
def get_user_hours(user, event_type):
  """Gets the specified user's hours and returns a timedelta object."""
  rset = RSVP.objects.filter(user=user, occurrence__event__event_type=event_type)
  duration = datetime.timedelta(0)
  for rsvp in rset:
    duration += rsvp.duration
  return duration
  
def check_standing(user, event_type):
  return get_user_hours(user.id, event_type.id) >= event_type.quota

# 
# def get_occurrences_or_events():
#   """docstring for get_occurrence_or_event"""
#   day = lambda occurrence: occurrence.start_time.day
#   event = lambda occurrence: 
#   occurrences = Occurrence.objects.all()
#   gr_oc = [(day, list(items)) for day, items in groupby(occurrences, day)]
#   for day in gr_oc:
#     
  
  