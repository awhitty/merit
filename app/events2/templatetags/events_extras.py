import datetime
# from datetime import datetime, timedelta

from django import template
from django.utils.timesince import timesince
from django.contrib.auth.models import User

from events.models import Occurrence, RSVP, EventType


# TODO: new format date
# Sunday, July 31 11:30 am - 3 pm 
# Tomorrow 11:30 am - 3 pm 
# Today 11:30 am - 3 pm 

register = template.Library()

def do_add_button(user_id, occurrence_id, occ_page=None):
  # TODO: rework add button to use multiple templates
  # one template for RSVP
  # one template for remove
  # one template for verify
  now = datetime.datetime.now()
  passed = False
  try:
    oc = Occurrence.objects.get(pk=occurrence_id)
    user = User.objects.get(pk=user_id)
  except:
    return ''
  rsvped = user in oc.users.all()
  if oc.start_time < now:
    passed = True
  if rsvped:
    rsvp = RSVP.objects.get(occurrence=oc,user=user)
    return {'rsvped': rsvped, 'rsvp': rsvp, 'passed': passed, 'occ_page': occ_page}
  else:
      return {'occurrence': oc, 'rsvped':rsvped, 'passed': passed, 'occ_page': occ_page}
  
def timedelta(value, arg=None):
    if not value:
        return ''
    if arg:
        cmp = arg
    else:
        cmp = datetime.datetime.now()
    if value > cmp:
        return "in %s" % timesince(cmp,value)
    else:
        return "%s ago" % timesince(value,cmp)
        
def format_timedelta(value, arg=None):
  h = value.days*24 + value.seconds // 3600 
  m = (value.seconds % 3600) // 60
  comma = True
  hstr, mstr = '', ''
  # is it 0?
  hstr = pluralize(h, 'hour')
  if m != 0:
    mstr = pluralize(m, 'minute')
  if h == 0 or m == 0:
    comma = False
    
  if comma == False:
    return '%s%s' % (hstr, mstr)
  else:
    return '%s, %s' % (hstr, mstr)
    
def pluralize(value, unit, unit_funk=None):
  if value == 1:
    return '%s %s' % (value, unit)
  else:
    return '%s %ss' % (value, unit)
  
def get_hours(user, type=None):
  # TODO: get hours as a percentage for graphing
  if not type:
    et = EventType.objects.all()
  else:
    et = EventType.objects.get(type)
  
  dur = []
  for i in et:
    duration = datetime.timedelta(0)
    rset = RSVP.objects.verified().filter(user=user, occurrence__event__event_type=i)
    for r in rset:
      duration += r.duration
    dur.append(duration)
    a = zip(et, dur)
  try:
    return {'zipped_list': a,}
  except:
    print 'No event types exist.'
    
def get_single_hours(user, type):
  duration = datetime.timedelta(0)
  rset = RSVP.objects.verified().filter(user=user, occurrence__event__event_type=type)
  for r in rset:
    duration += r.duration
  
  return {'duration': duration,}
    

register.filter('timedelta',timedelta)
register.filter('format_timedelta',format_timedelta)
register.inclusion_tag('includes/hour_list.html')(get_hours)
register.inclusion_tag('includes/single_hour.html')(get_single_hours)
register.inclusion_tag('includes/add_button.html')(do_add_button)