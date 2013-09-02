from django import template

from calendar import HTMLCalendar
from datetime import date
from itertools import groupby
import datetime

from django.utils.html import conditional_escape as esc
from django.utils.dateformat import DateFormat
from django.template.loader import render_to_string

from events.models import Occurrence

register = template.Library()

class EventCalendar(HTMLCalendar):

    def __init__(self, occurrences):
        super(EventCalendar, self).__init__()
        self.setfirstweekday(6)
        self.occurrences = self.group_by_day(occurrences)

    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            if date.today() == date(self.year, self.month, day):
                cssclass += ' today'
            if day in self.occurrences:
                cssclass += ' filled'
                body = ['<ul>']
                efield = lambda occurrence: occurrence.event
                grouped_occurrences = dict([(event, list(items)) for event, items in groupby(self.occurrences[day], efield)])
                for x, y in grouped_occurrences.iteritems():
                  if len(y) > 1:
                    body.append(render_to_string('includes/calendar_item.html', { 'object': x }))
                  else:
                    body.append(render_to_string('includes/calendar_item.html', { 'object': y[0] }))
                # for occurrence in self.occurrences[day]:
                #     df = DateFormat(occurrence.start_time)
                #     body.append('<span><li>')
                #     # body.append('<span class="time">%s</span>' % (df.format('P')))
                #     body.append('<a href="%s" style="background-color: #%s">' % (occurrence.get_absolute_url(), occurrence.event.event_type.color))
                #     body.append(esc(occurrence.title))
                #     body.append('</a></li></span>')
                body.append('</ul>')
                return self.day_cell(cssclass, '%d %s' % (day, ''.join(body)))
            return self.day_cell(cssclass, day)
        return self.day_cell('noday', '&nbsp;')

    def formatmonth(self, year, month):
        self.year, self.month = year, month
        return super(EventCalendar, self).formatmonth(year, month)

    def group_by_day(self, occurrences):
        field = lambda occurrence: occurrence.start_time.day
        return dict(
            [(day, list(items)) for day, items in groupby(occurrences, field)]
        )

    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)
        
def do_calendar(year, month, filter=None):
  if filter:
    occurrences = Occurrence.objects.public().order_by('start_time').filter(
      start_time__year=year, start_time__month=month, event__event_type__slug=filter,
      )
  else:
    occurrences = Occurrence.objects.public().filter(
      start_time__year=year, start_time__month=month,
      )
  cal = EventCalendar(occurrences).formatmonth(year, month)
  return {'calendar': cal,}
        
register.inclusion_tag('includes/calendar_view.html')(do_calendar)