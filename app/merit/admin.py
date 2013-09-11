
from django.contrib import admin

from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatPageAdmin

from pagedown.widgets import AdminPagedownWidget

class MarkdownFlatPageAdmin(FlatPageAdmin):

	def formfield_for_dbfield(self, db_field, **kwargs):
		if db_field.name == 'content':
			kwargs['widget'] = AdminPagedownWidget

		return super(MarkdownFlatPageAdmin, self).formfield_for_dbfield(db_field,**kwargs)


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, MarkdownFlatPageAdmin)