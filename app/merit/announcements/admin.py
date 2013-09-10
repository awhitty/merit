from django.contrib import admin
from django.db import models

from models import Announcement
from forms import AnnouncementForm

from pagedown.widgets import AdminPagedownWidget

from attachments.admin import AttachmentInlines


class AnnouncementAdmin(admin.ModelAdmin):
  list_display = ('title', 'author', 'published',)
  list_filter = ('author','published',)

  inlines = [AttachmentInlines]

  prepopulated_fields = {'slug': ('title',)}
  fieldsets = (
    ('', {
      'fields': ('title', 'slug', 'author',)
    }),
    ('', {
      'fields': ('body',)
    }),
    ('Date', {
      'classes': ('collapse closed',),
      'fields': ('published', )
    }),
  )
  
  formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget },
    }
  # 
  # class Media:
  #   js = ( '/media/wmd/wmd.js', )
      
admin.site.register(Announcement, AnnouncementAdmin)