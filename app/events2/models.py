import datetime
import timedelta

from django.db import models
from django.contrib.auth.models import User, Group

from denorm import denormalized, depend_on_related

class EventType(models.Model):
    """
    A type of event (e.g. community service)
    """

    title       = models.CharField(max_length=100)
    slug        = models.SlugField()
    quota       = timedelta.TimedeltaField()
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

    def __unicode__(self):
        return self.name

class CustomUser(User):
    class Meta:
            proxy = True

    @staticmethod 
    def autocomplete_search_fields(): 
        return ("id__iexact", "username__icontains", "first_name__icontains", "last_name__icontains") 


#===========================================================================   
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
        
    @staticmethod
    def autocomplete_search_fields():
        return ("title__icontains", "place__name__icontains",)

    @models.permalink
    def get_absolute_url(self):
            return ('event-detail', [self.slug])

#===========================================================================

class PublicOccurrenceManager(models.Manager):
        def get_query_set(self):
                return super(PublicOccurrenceManager, self).get_query_set().filter(event__hide=False)

class Occurrence(models.Model):
    """
    Represents the start and end time for a specific occurrence of a master Event object.
    """

    start_date     = models.DateField(default=datetime.datetime.today)
    alt_start_time = models.TimeField(('alternate start time'), blank=True, null=True)
    alt_end_time   = models.TimeField(('alternate end time'), blank=True, null=True)
    event          = models.ForeignKey(Event, verbose_name=('event'))
    users          = models.ManyToManyField(CustomUser, through='RSVP')

    public = PublicOccurrenceManager()

    def save(self, *args, **kwargs):
        super(Occurrence, self).save(*args, **kwargs)
        if self.event.required:
            from events.helpers import create_rsvp
            for user in User.objects.all():

                create_rsvp(user, self)
        

    @staticmethod
    def autocomplete_search_fields():
        return ("event__title__icontains", "start_date__icontains",)

    #===========================================================================
    class Meta:
            verbose_name = ('occurrence')
            verbose_name_plural = ('occurrences')
            ordering = ('start_time', 'end_time')
    
    #---------------------------------------------------------------------------
    def __unicode__(self):
        format = "%A, %B %d at %X"
        return u'%s: %s' % (self.title, self.start_time.strftime(format))
    
    #---------------------------------------------------------------------------
    @models.permalink
    def get_absolute_url(self):
            return ('events:occurrence-detail', [self.event.slug, self.id])
    
    #---------------------------------------------------------------------------
    def __cmp__(self, other):
            return cmp(self.start_time, other.start_time)
            
    #---------------------------------------------------------------------------
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

    @denormalized(models.CharField, max_length=400)
    def tags(self):
        t = ""
        time = self.start_time if not self.alt_start_time else datetime.datetime.combine(self.start_date, self.alt_start_time)

        # Time of day
        if(time.time() < datetime.time(12,0,0,0)):
            t += "morning "
        elif (time.time() < datetime.time(17,0,0,0)):
            t += "afternoon "
        else:
            t += "evening "

        # School period
        if self.event.period:
            t += "period-" + str(self.event.period) + " "

        # Event type
        t += self.event.event_type.slug + " "

        # Day of the week
        t += "day-" + time.strftime('%a').lower() + " "

        return t
    
    #---------------------------------------------------------------------------
    @denormalized(timedelta.TimedeltaField)
    def duration(self):
        if self.end_time > self.start_time:
            return (self.end_time - self.start_time)
        else:
            return (self.start_time - self.end_time)
    
    #---------------------------------------------------------------------------
    @property
    def title(self):
            return self.event.title

    #---------------------------------------------------------------------------
    @property
    def description(self):
            return self.event.description
    
    #---------------------------------------------------------------------------
    @property
    def event_type(self):
            return self.event.event_type
    
    #---------------------------------------------------------------------------
    @property
    def required(self):
            return self.event.required
    #---------------------------------------------------------------------------
    @property
    def date(self):
        format = "%A, %B %d"
        return u'%s' % (self.start_time.strftime(format))
        
    #---------------------------------------------------------------------------
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
    user          = models.ForeignKey(CustomUser)
    occurrence    = models.ForeignKey(Occurrence)
    alt_duration  = timedelta.TimedeltaField(blank=True, null=True)
    verified      = models.BooleanField(default=False)
    verified_date = models.DateTimeField(blank=True, null=True)
        
    class Meta:
        verbose_name = 'RSVP'
        unique_together = ("user", "occurrence")

    def save(self, *args, **kwargs):
        try:
            if self.verified and self.verified_date is None:
                self.verified_date = datetime.datetime.now()
        except:
            print 'No RSVP'
        
        self.tag = str(self.occurrence.title).lower()[:3] + str(self.user.username).lower()[:3] + str(self.occurrence.id)
        super(RSVP, self).save(*args, **kwargs)

    @denormalized(timedelta.TimedeltaField)
    @depend_on_related('Occurrence', foreign_key='occurrence')
    def duration(self):
        if self.alt_duration:
            return self.alt_duration
        return self.occurrence.duration

    @denormalized(models.DateTimeField)
    @depend_on_related('Occurrence', foreign_key='occurrence')
    def date(self):
        return self.occurrence.start_time
        
    @property
    def title(self):
        return self.occurrence.title
            

    @staticmethod
    def autocomplete_search_fields():
        return ("user__iexact", "name__icontains",)

    def __unicode__(self):
        format = "%A, %B %d"
        return u'%s to %s on %s' % (self.user, self.occurrence.event, self.occurrence.start_time.strftime(format),)
