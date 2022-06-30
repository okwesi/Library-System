from django.contrib import admin

from library_app.models import Librarian, Library

# Register your models here.

admin.site.register(Library)
admin.site.register(Librarian)