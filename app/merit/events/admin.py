from django.contrib import admin

from fields import formfield_callback

from models import *
# from widgets import SelectTimeWidget

# from pagedown.widgets import AdminPagedownWidget

# from attachments.admin import AttachmentInlines

class RSVPInline(admin.TabularInline):
    classes = ('collapse open',)
    fields = ('user', 'alt_duration', 'duration', 'verified', 'verified_date')
    readonly_fields = ('duration', 'verified_date')

    raw_id_fields = ('user',)

    autocomplete_lookup_fields = {
                'fk': ['user'],
        }

    model = RSVP
    
class OccurrenceInline(admin.TabularInline):
    fields = ('start_date','alt_start_time', 'alt_end_time')
    search_fields = ('event',)
    model = Occurrence
    extra = 0
    
class RSVPAdmin(admin.ModelAdmin):
    search_fields = ('tag','user__username','occurrence__event__title')
    list_display = ('user','occurrence','tag', 'duration', 'alt_duration', 'verified')
    list_filter  = ('occurrence','user')
    list_editable = ('alt_duration', 'verified')
    fields = ('user','occurrence', 'alt_duration', 'duration', 'tag', 'verified', 'verified_date')
    readonly_fields = ('duration', 'tag', 'verified_date')
    actions = ['verify',]

    raw_id_fields = ('user','occurrence')

    autocomplete_lookup_fields = {
                'fk': ['user','occurrence'],
        }

    def verify(self, request, queryset):
        for rsvp in queryset:
            rsvp.verified = True
            rsvp.save()
        self.message_user(request, "Each RSVP was verified.")

    verify.short_description = 'Verify selected RSVPs'
    
class EventAdmin(admin.ModelAdmin):
    prepopulated_fields   = {'slug': ('title',)}
    inlines               = [OccurrenceInline]
    list_display          = ('title','event_type','place','default_start_time', 'required',)
    list_filter           = ('event_type','place','required')
    search_fields         = ('title', 'place__name')
    actions               = ['feature']
    fieldsets = (
        ('', {
            'fields': ('title', 'slug','event_type',)
        }),
        ('', {
            'fields': ('place','capacity','period', 'required', 'hide')
        }),
        ('', {
            'fields': ('description','default_start_time','default_end_time')
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        # Somehow we set the formfield callback here?
        return super(EventAdmin, self).get_form(request, obj, **kwargs)

    # formfield_overrides = { models.TextField: {'widget': AdminPagedownWidget }, }
     

class OccurrenceAdmin(admin.ModelAdmin):
    search_fields = ('event__title','event__place__name',)
    list_display   = ('event','start_date', 'start_time','end_time',)
    list_filter    = ('event','start_time','end_time','event__event_type')
    list_editable  = ('start_date',)
    readonly_fields = ('start_time', 'end_time',)
    date_hierarchy = 'start_time'
    fields         = ('start_date','event', 'alt_start_time', 'alt_end_time', 'start_time', 'end_time',)
    inlines        = [RSVPInline]

    raw_id_fields = ('event',)

    autocomplete_lookup_fields = {
                'fk': ['event'],
        }

    
class EventTypeAdmin(admin.ModelAdmin):
    prepopulated_fields   = {'slug': ('title',)}

class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name','address','city','state','zip','latitude','longitude',)
        
        
# admin.site.register(CustomUser)
admin.site.register(Event, EventAdmin)
admin.site.register(Place, PlaceAdmin)
admin.site.register(RSVP, RSVPAdmin)
admin.site.register(EventType, EventTypeAdmin)
admin.site.register(Occurrence, OccurrenceAdmin)
