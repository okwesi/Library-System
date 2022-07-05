
from django.conf.urls import url, include
from django.urls.conf import path, re_path
from . views import *
urlpatterns = [    
    path('school-request/<uuid:book_id>/',school_request, name="school-request-book"), 
    path('approve/<uuid:school_id>', approve_requests , name="approve_requests"),
    path('return/<uuid:school_id>/', return_requests , name="return_requests"),
    path('school-request/requests', school_all_requests , name="approve_requests"),
    
    
    path('student-request/<uuid:book_id>/',student_request, name="student-request-book"), 
    
     
    path('librarian_get_student_request/',librarian_student_request, name="librarian_get_student_request"),
    path('librarian_get_grouped_requests/', librarian_requests, name="librarian_get_grouped_request"), 
    path('librarian_get_grouped_received/', librarian_received, name="librarian_get_grouped_received"), 
    path('details/<uuid:school_id>/', librarian_get_request_details , name="request-details"),
    path('details/received/<uuid:school_id>/', librarian_get_received_details , name="received-details"),
    # path('return/<uuid:school_id/', return_requests , name="returned_requests"),
    # path('approve/<uuid:school_id/', approve_requests , name="approve_requests"),
    path('requests/', School_requests , name="school_requests"),
    
    path('school/approved/', school_approved_requests, name="school_approved_requests"),
    path('school/received/', school_received_requests, name="school_received_requests"),
    path('school/set_received/', School_set_received, name="set_received_requests")
     
] 