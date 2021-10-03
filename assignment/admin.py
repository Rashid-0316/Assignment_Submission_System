from django.contrib import admin
from django.contrib.admin.decorators import register
from .models import *
# # Register your models here.

admin.site.register(Department)
# admin.site.register(User)
# admin.site.register(StudentUser)
admin.site.register(User)
admin.site.register(HOD_User)
admin.site.register(Teacher_User)
admin.site.register(Clerk_User)
admin.site.register(Student_User)
