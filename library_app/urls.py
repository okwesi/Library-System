
from django.conf.urls import url, include
from django.urls.conf import path
from . views import(
        get_schools, 
        super_dashboard_view,
        librarians_query,
        librarian_dashboard_view,
        delete_librarian)


urlpatterns = [    
        url('super-dashboard', super_dashboard_view, name='library_admin'),
        url('librarian-dashboard', librarian_dashboard_view, name='librarian_dashboard'),
        url('query-librarians/', librarians_query, name='query-librarians'),   
        path(r'delete_librarian/<uuid:librarian_id>/', delete_librarian, name="delete_librarian"),
        url('get-schools/', get_schools, name='get-schools'),   
] 