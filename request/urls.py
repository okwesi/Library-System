
from django.conf.urls import url, include
from django.urls.conf import path
from . views import(
approve_requests, 
librarian_requests, 
librarian_student_request,
school_all_requests, 
student_request,
school_request,
librarian_get_request_details,
approved_requests,
)
urlpatterns = [    
    path('school-request/<uuid:book_id>/',school_request, name="school-request-book"), 
    path('approve/<uuid:school_id>', approve_requests , name="approve_requests"),
    path('school-request/requests', school_all_requests , name="approve_requests"),
    
    
    path('student-request/<uuid:book_id>/',student_request, name="student-request-book"), 
    
     
    path('librarian_get_student_request/',librarian_student_request, name="librarian_get_student_request"),
    path('librarian_get_grouped_requests/', librarian_requests, name="librarian_get_grouped_request"), 
    path('details/<uuid:school_id>/', librarian_get_request_details , name="request-details"),
    # path('approve/<uuid:school_id/', approve_requests , name="approve_requests"),
    path('approved/', approved_requests , name="approved_requests"),
     
] 