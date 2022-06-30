from multiprocessing import context
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from books.models import Book
from request.forms import SchoolRequestForm
from students_school.models import Student
import json
from users.models import User
from .forms import StudentForm
# Create your views here.
def create_student( request):
    pass


 
def school_dashboard(request):
    students = Student.objects.filter(school_id=request.user.school.school_id)
    count = students.count
    
    return render(request, 'school/school_dashboard.html', {"count": count})

def school_get_students(request):
    students = Student.objects.filter(school_id=request.user.school.school_id)
    count = students.count
    data = []
    for student in students: 
        student_data = {
            'id': student.student_id,
            'name' : student.name,
            'email': student.user.email,
            'phone': student.user.phone,
            'city': student.city,
            'address': student.address,
            'gps_location' : student.gps_location,
            'school_class' : student.school_class,
            'gender' : student.gender
        }
        data.append(student_data)
    
    return JsonResponse(
        {
        'data' : data,
        }
    ) 
    
    

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