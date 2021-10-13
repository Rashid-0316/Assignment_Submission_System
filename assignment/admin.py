from django.contrib import admin
from django.contrib.admin.decorators import register
from .models import *

admin.site.register(Department)
admin.site.register(User)
admin.site.register(HOD_User)
admin.site.register(Teacher_User)
admin.site.register(Clerk_User)
admin.site.register(Student_User)
admin.site.register(Batch)
admin.site.register(Semester)
admin.site.register(Course)
# admin.site.register(Subject)