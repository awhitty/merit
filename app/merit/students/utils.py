from models import Student

def get_or_create_user_profile(user):
    profile = None
    user = user
    try:
        profile = user.get_profile()
    except UserProfile.DoesNotExist:
        profile = Student.objects.create(user)
    return profile