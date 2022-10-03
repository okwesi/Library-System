
# from django.conf.urls import url, include
from django.urls.conf import path
from . views import *

urlpatterns = [    
        path('super-dashboard', super_dashboard_view, name='library_admin'),
        path('librarian-dashboard', librarian_dashboard_view, name='librarian_dashboard'),
        path('query-librarians/', librarians_query, name='query-librarians'),   
        path(r'delete_librarian/<uuid:librarian_id>/', delete_librarian, name="delete_librarian"),
        path('get-schools/', get_schools, name='get-schools'),   
        path('get_new_books/', get_new_books, name='get_new_books'),   
] 