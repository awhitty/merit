from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from models import Student

class StudentInline(admin.StackedInline):
	model = Student
	can_delete = False
	verbose_name_plural = 'student'

class UserProfileAdmin(UserAdmin):
	list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'class_year')
	inlines = (StudentInline, )
	search_fields = UserAdmin.search_fields + ('student__class_year',)
	list_filter = UserAdmin.list_filter + ('student__class_year',)

	def class_year(self, obj):
		return obj.get_profile().class_year

	# search_fields = UserAdmin.search_fields + ('class_year',)

admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)