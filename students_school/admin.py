from django.contrib import admin

from students_school.models import School, Student

# Register your models here.
class SchoolAdmin(admin.ModelAdmin):
    readonly_fields = ('school_number',)

admin.site.register(School, SchoolAdmin)

admin.site.register(Student)

# admin.site.register(School)
