
from unicodedata import name
# from django.conf.urls import url
from django.urls.conf import path,re_path
from . views import *


urlpatterns = [
        path('add/', add_book, name="add_books"),
        # url('add-book/', BookAddView.as_view(), name="add-books"),
        path('get-books/', LibrarianBookListView.as_view(), name="get-books"),
        
        
        re_path(r'^$', PublicBookListView.as_view(), name="public-books"),
        path('<uuid:id>/', book_detail, name="book-detail"), 

         
        path('<uuid:id>/', book_detail, name="book-detail"), 
        path('<uuid:book_id>/update', edit_book, name="edit-book"), 
        path('<uuid:book_id>/delete', delete_book, name="delete-book"), 
        
        path('libraries/', public_get_libraries, name="public_get_libraries"),
        path('books/<uuid:library_id>/', get_public_books, name="get_public_books"),

] 