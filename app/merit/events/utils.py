from models import RSVP

# create_rsvp
# destroy_rsvp
# verify_rsvp

def create_rsvp(user, occurrence):
	rsvp = RSVP(user=user, occurrence=occurrence)
	rsvp.save()

def destroy_rsvp(rsvp):
	rsvp.delete()