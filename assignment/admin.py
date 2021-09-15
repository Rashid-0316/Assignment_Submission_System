from django.contrib import admin
from .models import User,StudentUser,Department
# Register your models here.

admin.site.register(Department)
admin.site.register(User)
admin.site.register(StudentUser)
