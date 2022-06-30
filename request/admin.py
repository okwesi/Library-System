from django.contrib import admin

from request.models import SchoolRequests, StudentRequests

# Register your models here.
admin.site.register(StudentRequests)
admin.site.register(SchoolRequests)