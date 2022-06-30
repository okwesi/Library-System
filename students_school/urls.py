from django.conf.urls import url, include
from django.urls.conf import path
from . views import *


urlpatterns = [    
        url('student/create-profile/', create_student, name='create_student_profile'),
        url('school-dashboard/', school_dashboard, name='school-dashboard'),
        url('get_students/', school_get_students, name="get_students"),
        url('school/bookshelf/', school_bookshelf, name="school-bookshelf"),
        path(r'school/get_books/<int:num_books>/', get_school_books, name="get-student-books"),
        path('school/<uuid:id>/', school_book_detail, name="student-book-detail"), 
        
        
        
        
        
        path('student/<uuid:id>/', student_book_detail, name="student-book-detail"), 
        # url('student/bookshelf/', student_bookshelf, name="student-bookshelf"),
        path(r'student/get_books/<int:num_books>/', get_student_books, name="get-student-books"),
]  