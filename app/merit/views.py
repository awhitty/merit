from app.main.decorators import render_to

@render_to('merit/index.html')
def index(request):
    pass

@render_to('merit/occurrences.html')
def occurrences(request):
    pass

@render_to('merit/occurrence.html')
def occurrence(request):
    pass

@render_to('merit/rsvps.html')
def rsvps(request):
    pass

@render_to('merit/stats.html')
def stats(request):
    pass

# change password
# flat pages
# announcements?
# 