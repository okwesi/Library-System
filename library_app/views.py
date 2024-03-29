import json
import random
from base64 import urlsafe_b64encode
from email.message import EmailMessage
from datetime import date

# time import_fresh_module
from books.forms import BookForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.sites.shortcuts import get_current_site
from django.core import serializers
from django.core.mail import EmailMessage, send_mail
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils import timezone
# from django.utils.encoding import force_bytes, force_text

from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from books.models import Book, NewBooks
from request.models import SchoolRequests, StudentRequests
from students_school.models import School, Student
from users.forms import SignSchoolUpForm
from users.models import User

from library_app.forms import LibrarianForm
from library_app.models import Librarian, Library

# Create your views here.

def super_dashboard_view(request):
    school = School.objects.filter(library=request.user.librarian.library).count()
    books = Book.objects.filter(library=request.user.librarian.library).count()
    # librarian = Librarian.objects.filter(library=request.user.librarian.library).count()
    student_requests = StudentRequests.objects.filter(library=request.user.librarian.library).count()
    school_requests = SchoolRequests.objects.filter(library=request.user.librarian.library).count()
    requests = StudentRequests.objects.raw(f"select id,school_id,   count(*) count from (select id,school_id, status, student_id, request_date from request_studentrequests where library_id='{request.user.librarian.library.id.hex}') group by school_id ")
    category_data = StudentRequests.objects.raw(f"select  id, book_id, count(*) as number_of_request, name, category_id from (select * from request_studentrequests join (select books_book.id as book_id, books_category.id as category_id, books_category.name from books_book join books_category on books_book.category_id = books_category.id) book  on request_studentrequests.book_id = book.book_id where request_studentrequests.library_id='{request.user.librarian.library.id.hex}') group by category_id")
    books_data = StudentRequests.objects.raw(f"select request_studentrequests.id , request_studentrequests.library_id, request_studentrequests.book_id, books_book.title, count(*) as number from request_studentrequests join books_book on request_studentrequests.book_id = books_book.id where request_studentrequests.library_id = '{request.user.librarian.library.id.hex}' group by request_studentrequests.book_id")
    date_data = StudentRequests.objects.raw(f"select id,count(*) as number, strftime('%m-%Y', request_date) as 'month_year' from request_studentrequests where library_id='{request.user.librarian.library.id.hex}' group by strftime('%m-%Y', request_date)  order by  strftime('%m-%Y', request_date) asc")
    
    context = {
        "school":school,
        "books":books,
        # "librarian" : librarian,
        "student_requests":student_requests,
        "school_requests": school_requests,
        "requests" :requests, 
        "category_data":category_data[:5],
        "books_data" : books_data[:6],
        "date_data" : date_data[:8]
    }

    return render(request, "librarian/overview.html", context)

# converts time date
def convert_to_localtime(utctime):
  fmt = '%d/%m/%Y %H:%M'
  utc = utctime.replace(tzinfo=pytz.UTC)
  localtz = utc.astimezone(timezone.get_current_timezone())
  return localtz.strftime(fmt)


def librarians_query(request):
    
    librarians = Librarian.objects.filter(library_id=request.user.librarian.library.id).exclude(id=request.user.librarian.id)
    # # .exclude(id=request.user.librarian.id)
    # data = []
    # for librarian in librarians:
    #     librarian_data = {
    #         'name': librarian.full_name,
    #         'email' : librarian.user.email,
    #         'phone' : librarian.user.phone,
    #         'last_login' : convert_to_localtime(librarian.user.last_login),
    #         'group' : str(librarian.user.groups.all()[0])
    #     }
    #     data.append(librarian_data)
    # return JsonResponse({'data':data})
    return render(request, "librarian/librarians.html", {'librarians':librarians})




def librarian_dashboard_view(request):
    """function for creating forms to add users then sends a verification link to the email of the user"""
    bookForm = BookForm()   
    librarian = "function for creating forms to add users then sends a verification link to the email of the user"
    context = {
        "bookForm" : bookForm,
        "librarian" : librarian
    }
    
    return render(request, "library/librarian_dashboard.html", context)



def get_schools(request):
    schools = School.objects.filter(library=request.user.librarian.library_id)
    return render(request, "librarian/schools.html", {"schools":schools})


def get_new_books(request):
    new_books = NewBooks.objects.filter(library_id=request.user.librarian.library.id)
    grouped_new_books = NewBooks.objects.raw(f"select *, count(*) as count from books_newbooks where library_id = '{request.user.librarian.library.id.hex}' group by lower(name)")
    return render(request, "librarian/new_books.html", {"new_books":new_books, "grouped_new_books":grouped_new_books})



def delete_librarian(request, librarian_id):
    librarian = Librarian.objects.get(id=librarian_id)
    user = User.objects.get(id=librarian.user.id)
    user.delete()    
    return JsonResponse({})




#  # request.is_ajax() and 
#     if request.method == "POST":
#         libraryForm = LibrarianForm(request.POST or None)
#         if libraryForm.is_valid():            
#             #save form in the memory not in database
#             user = libraryForm.save()
#             #adds a group to the user
#             user_group = Group.objects.get(name='librarian')
#             user.groups.add(user_group)
#             user.save()
#             Librarian.objects.create(
#                 user=user, 
#                 full_name=libraryForm.cleaned_data.get("full_name"),
#                 library = request.user.librarian.library
#             )

#             current_site = get_current_site(request)  
#             mail_subject = 'Activation link has been sent to your email id'  
#             message = render_to_string('users/acc_active_email_librarians.html', {  
#                 'user': user,  
#                 'domain': current_site.domain,  
#                 'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
#                 "userpassword" :  libraryForm.cleaned_data.get('password1')
#             })  
#             to_email = libraryForm.cleaned_data.get('email')  
#             email = EmailMessage(  
#                         mail_subject, message, to=[to_email]  
#             )  
#             email.send()
            
#             return JsonResponse({
#                 'id': user.id,
#                 'name': libraryForm.cleaned_data.get("full_name"),
#                 'email' : libraryForm.cleaned_data.get("email"),
#                 'phone' : libraryForm.cleaned_data.get("phone"),
#                 'last_login' : "Not Yet",
#                 'group' : 'librarian'
#             })
