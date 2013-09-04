import datetime, timedelta, urllib, urllib2

from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.encoding import smart_str
from django.utils import simplejson

from denorm import denormalized, depend_on_related

class EventType(models.Model):
    """
    A type of event (e.g. community service)
    """

    title       = models.CharField(max_length=100)
    slug        = models.SlugField()
    quota       = timedelta.fields.TimedeltaField()
    description = models.TextField(blank=True)
    is_total    = models.BooleanField(blank=True, default=False, help_text='Is this quota for total hours?')

    def __unicode__(self):
        return self.title
        
    @models.permalink
    def get_absolute_url(self):
            return ('events:event-type-detail', [self.slug])

class Place(models.Model):
    """
    Where an event takes place.
    """

    name    = models.CharField(max_length=100)
    address = models.CharField(max_length=200, blank=True, null=True)
    city    = models.CharField(max_length=100, blank=True, null=True)
    state   = models.CharField(max_length=4, default="CO")
    zip     = models.PositiveIntegerField(max_length=10, blank=True, null=True)

    latitude  = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __unicode__(self):
        return self.name

    def save(self):
        
        # Because google seems to get confused sometimes...
        if self.address:
            location = "%s, %s, %s, %s" % (self.address, self.city, self.state, self.zip)
        else:
            location = "%s, %s" % (self.name, self.state)

        if not self.latitude or not self.longitude:
            latlng = self.geocode(location)
            if latlng:
                latlng = latlng.split(',')
                self.latitude = float(latlng[0])
                self.longitude = float(latlng[1])

        super(Place, self).save()

    def geocode(self, location):
        location = urllib.quote_plus(smart_str(location))
        request = "http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false" % (location)
        response = urllib2.urlopen(request).read() 
        result = simplejson.loads(response)
        if result['status'] == 'OK':
            lat = str(result['results'][0]['geometry']['location']['lat'])
            lng = str(result['results'][0]['geometry']['location']['lng'])
            return '%s,%s' % (lat, lng)
        else:
            return ''


class Event(models.Model):
    """
    Something that can occur.
    """

    title              = models.CharField(max_length=100)
    slug               = models.SlugField(unique=True)
    place              = models.ForeignKey(Place)
    period             = models.PositiveIntegerField(help_text=('If this event occurs during school, which period?'), blank=True, null=True)
    event_type         = models.ForeignKey(EventType)
    required           = models.BooleanField(help_text=('Is attendance required? Careful, checking this button will RSVP every member.'), default=False, blank=True)
    hide               = models.BooleanField(help_text=('Should this be shown on the events page?'), default=False, blank=True)
    description        = models.TextField(blank=True, help_text=('google \"Markdown\" for formatting tips'))
    capacity           = models.PositiveIntegerField(blank=True, null=True, help_text=('How many volunteers can sign up?'))
    default_start_time = models.TimeField()
    default_end_time   = models.TimeField()

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
            return ('event-detail', [self.slug])

class OccurrenceManager(models.Manager):
    def public(self):
        return self.get_query_set().filter(event__hide=False)


class Occurrence(models.Model):
    """
    Represents the start and end time for a specific occurrence of a master Event object.
    """

    start_date     = models.DateField(default=datetime.datetime.today)
    alt_start_time = models.TimeField(('alternate start time'), blank=True, null=True)
    alt_end_time   = models.TimeField(('alternate end time'), blank=True, null=True)
    event          = models.ForeignKey(Event, verbose_name=('event'))
    users          = models.ManyToManyField(User, through='RSVP')

    tags = models.TextField(null=True)

    objects = OccurrenceManager()

    def save(self, *args, **kwargs):
        super(Occurrence, self).save(*args, **kwargs)
        if self.event.required:
            from events.helpers import create_rsvp
            for user in User.objects.all():
                create_rsvp(user, self)

    class Meta:
            verbose_name = ('occurrence')
            verbose_name_plural = ('occurrences')
            ordering = ('start_time', 'end_time')
    
    def __unicode__(self):
        format = "%A, %B %d at %X"
        return u'%s: %s' % (self.title, self.start_time.strftime(format))

    def __cmp__(self, other):
            return cmp(self.start_time, other.start_time)
    
    @models.permalink
    def get_absolute_url(self):
            return ('merit-occurrence', [self.event.slug, self.id])
            
    @denormalized(models.DateTimeField)   
    def start_time(self):
            if self.alt_start_time:
                return datetime.datetime.combine(self.start_date, self.alt_start_time)
            else:
                return datetime.datetime.combine(self.start_date, self.event.default_start_time)
    
    @denormalized(models.DateTimeField)   
    def end_time(self):
            if self.alt_end_time:
                return datetime.datetime.combine(self.start_date, self.alt_end_time)
            else:
                return datetime.datetime.combine(self.start_date, self.event.default_end_time)
    
    @denormalized(timedelta.fields.TimedeltaField)
    def duration(self):
        if self.end_time > self.start_time:
            return (self.end_time - self.start_time)
        else:
            return (self.start_time - self.end_time)
    
    @property
    def title(self):
            return self.event.title

    @property
    def description(self):
            return self.event.description
    
    @property
    def event_type(self):
            return self.event.event_type
    
    @property
    def required(self):
            return self.event.required
    @property
    def date(self):
        format = "%A, %B %d"
        return u'%s' % (self.start_time.strftime(format))
        
    @property
    def time(self):
        return (self.start_time, self.end_time)

    @property
    def is_full(self):
        return self.event.capacity and self.users.count() >= self.event.capacity

    @property
    def passed(self):
        return self.start_time < datetime.datetime.now()
    
#===========================================================================

class RSVP(models.Model):
    """
    A user's commitment to a particular occurrence.
    """
    
    tag           = models.CharField(max_length=10)
    user          = models.ForeignKey(User)
    occurrence    = models.ForeignKey(Occurrence)
    alt_duration  = timedelta.fields.TimedeltaField(blank=True, null=True)
    verified      = models.BooleanField(default=False)
    verified_date = models.DateTimeField(blank=True, null=True)
        
    class Meta:
        verbose_name = 'RSVP'
        unique_together = ("user", "occurrence")

    def __unicode__(self):
        format = "%A, %B %d"
        return u'%s to %s on %s' % (self.user, self.occurrence.event, self.occurrence.start_time.strftime(format),)

    def save(self, *args, **kwargs):
        try:
            if self.verified and self.verified_date is None:
                self.verified_date = datetime.datetime.now()
        except:
            print 'No RSVP'
        
        self.tag = str(self.occurrence.title).lower()[:3] + str(self.user.username).lower()[:3] + str(self.occurrence.id)
        super(RSVP, self).save(*args, **kwargs)
        
    @denormalized(timedelta.fields.TimedeltaField)
    @depend_on_related('Occurrence', foreign_key='occurrence')
    def duration(self):
        if self.alt_duration:
            return self.alt_duration
        return self.occurrence.duration

    @denormalized(models.DateTimeField)
    @depend_on_related('Occurrence', foreign_key='occurrence')
    def date(self):
        return self.occurrence.start_time
