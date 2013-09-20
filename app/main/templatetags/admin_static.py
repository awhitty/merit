from django.conf import settings
from django.template import Library

register = Library()

from django.contrib.staticfiles.templatetags.staticfiles import static

static = register.simple_tag(static)