import datetime

from django.db.models import permalink
from django.db import models
from django.contrib.auth.models import User
from django.contrib.markup.templatetags.markup import restructuredtext
from django.core.cache import cache
from django.utils.safestring import mark_safe

class Announcement(models.Model):
  """(Announcement description)"""
  title = models.CharField(max_length=200)
  slug = models.SlugField()
  author = models.ForeignKey(User)
  body = models.TextField(help_text=('google \"Markdown" for formatting tips'))
  published = models.DateTimeField(default=datetime.datetime.today)

  class Admin:
    list_display = ('',)
    search_fields = ('',)

  def __unicode__(self):
    return self.title
    
  def _get_content_html(self):
    key = 'announcement_html_%s' % str(self.pk)
    html = cache.get(key)
    if not html:
      html = restructuredtext(self.body)
      cache.set(key, html, 60*60*24*30)
    return mark_safe(html)
  content_html = property(_get_content_html)
  
  def save(self):
      if self.id:
        cache.delete('announcement_html_%s' % str(self.pk))
      super(Announcement, self).save()
    
  @permalink
  def get_absolute_url(self):
    return ('announcement_detail', None, { 'slug': self.slug } )