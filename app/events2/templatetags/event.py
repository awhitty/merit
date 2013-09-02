from django import template

register = template.Library()

@register.inclusion_tag('events/includes/occurrence_row.html')
def occurrence_row(request, occurrence):
	return {'request': request, 'occurrence': occurrence }

@register.inclusion_tag('events/includes/address.html')
def address(place, tags = True):
	return {'place': place, 'tags': tags }