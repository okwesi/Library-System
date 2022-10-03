from django.contrib import admin

from library_app.models import Librarian, Library
from users.models import User

# Register your models here.

class UserAdmin(admin.TabularInline):
    model = User
    
    
class LibrarianAdmin(admin.StackedInline):
    inlines = [UserAdmin ]
    model = Librarian
    extra = 3

class LibraryAdmin(admin.ModelAdmin):
   inlines = [LibrarianAdmin ]
#    list_display = ("text",'pub_date', "active")

admin.site.register(Library,LibraryAdmin)

# admin.site.register(Library)
# admin.site.register(Librarian)