from pagedown.widgets import AdminPagedownWidget
from django import forms
from announcements.models import Announcement

class AnnouncementForm(forms.ModelForm):
    title = forms.CharField(widget=AdminPagedownWidget())        
    body = forms.CharField(widget=AdminPagedownWidget())  

    class Meta:
        model = Announcement