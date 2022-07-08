from multiprocessing import context
import re
from urllib.request import Request
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from books.models import Book
from request.forms import SchoolRequestForm
from request.models import StudentRequests
from students_school.models import Student

# Create your views here.

 
def school_dashboard(request):
    students = Student.objects.filter(school_id=request.user.school.school_id)
    count = students.count
    
    return render(request, 'school/overview.html', {"count": count})

def school_get_students(request):
    students = Student.objects.filter(school_id=request.user.school.school_id)
    count = students.count
    data = []
    # for student in students: 
    #     student_data = {
    #         'id': student.student_id,
    #         'name' : student.name,
    #         'email': student.user.email,
    #         'phone': student.user.phone,
    #         'city': student.city,
    #         'address': student.address,
    #         'gps_location' : student.gps_location,
    #         'school_class' : student.school_class,
    #         'gender' : student.gender
    #     }
    #     data.append(student_data)
    
    # return JsonResponse(
    #     {
    #     'data' : data,
    #     }
    # ) 
    context = {
        "students" : students,
        "count" :  count
    }
    return render(request, 'school/students.html', context)
    
    

# def get_books(request):
#     books = Book.objects.filter(library_id=request.user.student.school.library.id)
#     return render(request, 'books/bookshelf.html', {"books":books})


def get_student_books(request, num_books):
    # todo: check if student has ordered and restict him
    
    visible = 3
    upper_bound = int(num_books)
    lower_bound = upper_bound - visible
    size = Book.objects.all().count
    books = Book.objects.filter(library_id=request.user.student.school.library.id)
    # .exclude(id=request.user.librarian.id)
    data = []
    for book in books:
        book_data = {
            "student" : request.user.student.name,
            'book_id' : book.id,
            'title': book.title,
            'about' : book.about,
            'stock' : book.stock,
            'library' : book.library.name,
        }
        data.append(book_data)
  
    return JsonResponse({'data':data[lower_bound:upper_bound]}, safe=False)


def student_book_detail(request, id):
    book = Book.objects.get(id=id)    
    context = {
        "book" : book,
    }
    return render(request, "student/student_book_detail.html", context)




def school_bookshelf(request):
    return render(request, 'school/bookshelf.html')


def get_school_books(request, num_books):
    # todo: check if school has ordered and restrict it
     
    visible = 3
    upper_bound = int(num_books)
    lower_bound = upper_bound - visible
    size = Book.objects.all().count
    books = Book.objects.filter(library_id=request.user.school.library.id)
    # .exclude(id=request.user.librarian.id)
    data = []
    for book in books:
        book_data = {
            "school" : request.user.school.name,
            'book_id' : book.id,
            'title': book.title,
            'about' : book.about,
            'stock' : book.stock,
            'library' : book.library.name,
        }
        data.append(book_data)
  
    return JsonResponse({'data':data[lower_bound:upper_bound]}, safe=False)


def school_book_detail(request, id):
    book = Book.objects.get(id=id) 
    request_form = SchoolRequestForm()   
    context = {
        "book" : book, 
        "request_form" : request_form       
    }
    return render(request, "school/school_book_detail.html", context)



def student_dashboard(request):
    books = StudentRequests.objects.filter(student=request.user.student)
    
    
    

####---------------------------------student dahsboard---------------------------

def get_book_history(request):
    books = StudentRequests.objects.filter(student_id=request.user.student.student_id)
    return render(request, "student/book_history.html", {"books":books})
    
def get_request_history(request):
    histories = StudentRequests.objects.filter(student_id=request.user.student.student_id, status="Returned")  
    return render(request, "student/request_history.html", {"histories":histories})
    
def get_ongoing_request(request):
    requests = StudentRequests.objects.filter(student_id=request.user.student.student_id).exclude(status="Returned")
    return render(request, "student/request_ongoing.html", {"requests":requests})