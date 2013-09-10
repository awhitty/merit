
from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
	user 	   = models.OneToOneField(User)
	class_year = models.PositiveIntegerField(blank=True, null=True, )