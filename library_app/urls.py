
# from django.conf.urls import url, include
from django.urls.conf import path
from . views import(
        get_schools, 
        super_dashboard_view,
        librarians_query,
        librarian_dashboard_view,
        delete_librarian)


urlpatterns = [    
        path('super-dashboard', super_dashboard_view, name='library_admin'),
        path('librarian-dashboard', librarian_dashboard_view, name='librarian_dashboard'),
        path('query-librarians/', librarians_query, name='query-librarians'),   
        path(r'delete_librarian/<uuid:librarian_id>/', delete_librarian, name="delete_librarian"),
        path('get-schools/', get_schools, name='get-schools'),   
] 