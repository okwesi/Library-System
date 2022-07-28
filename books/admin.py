from django.contrib import admin

from books.models import Book, Category

# Register your models here.
class BookAdmin(admin.ModelAdmin):
   list_display = ("title",'library', "stock")  
admin.site.register(Book,BookAdmin)

class CategoryAdmin(admin.ModelAdmin):
   list_display = ("name",'library')  
admin.site.register(Category,CategoryAdmin)

# admin.site.register(Category)