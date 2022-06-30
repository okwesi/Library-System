from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.core import serializers
from datetime import date


from books.models import Book
from request.forms import SchoolRequestForm
from request.models import SchoolRequests, StudentRequests
from students_school.models import School, Student

# Create your views here.

def student_request(request, book_id): 
    if request.method == "POST":
        user = request.user.student
        user.borrowed = True
        # print(user)
        book = get_object_or_404(Book, id=book_id)
        status = "Pending Approval";
        school = request.user.student.school
        
        student_request = StudentRequests(student=user, book=book, status=status, school=school )
        student_request.save()        
        user.save()
    return redirect("student-bookshelf")
        
    
    
#handles school request  for books
def school_request(request, book_id): 
    form = SchoolRequestForm(request.POST or None)
    # if request.method == "POST":
    if form.is_valid():
        print (form.cleaned_data.get("quantity"))
        requested_quantity = form.cleaned_data.get("quantity")
        user = request.user.school
        user.borrowed = True
        # print(user)
        book = get_object_or_404(Book, id=book_id)
        # TODO use Github Copilot
        if book.stock >= requested_quantity:
            book.stock = book.stock - requested_quantity
            status = "Pending Approval";
            quantity = requested_quantity
            
            school_request = SchoolRequests(school=user, book=book, status=status, quantity=quantity)
            school_request.save()        
            user.save()
            book.save()
            messages.success(request, "Book Requested successfully")
            return redirect("school-bookshelf")
        else:
            request_form = SchoolRequestForm()   
            context = {
                "book" : book, 
                "request_form" : request_form       
            }
            messages.error(request, "Book Request unsuccessful")
            return render(request, "school/school_book_detail.html", context)
    
   
   
   
   
   
   
        
#collect student request to the 
def librarian_student_request(request):
    student_requests = StudentRequests.objects.filter(status="Pending Approval")
    # .exclude(id=request.user.librarian.id)
    data = []
    for student_request in student_requests:
        student_request_data = {
            'id' : student_request.id,
            "book" : get_object_or_404(Book, id=student_request.book.id).title,
            "student" : get_object_or_404(Student, student_id=student_request.student.student_id).name,
            "school" : get_object_or_404(School, school_id=student_request.school.school_id).name
        }
        data.append(student_request_data)
    return JsonResponse({'data':data})

# Todo: https://www.bootdey.com/snippets/view/bs4-card-widget

def librarian_requests(request):
    requests = StudentRequests.objects.raw(f"select id,school_id, request_date,  count(*) count from (select id,school_id, status, student_id, request_date from request_studentrequests where status = 'Pending Approval' and request_date <= '{date.today()}') group by school_id ")
    return render(request, 'librarian/student.html', {"requests":requests})




def librarian_get_request_details(request, school_id):
    """gets book requests with Pending Approval status"""
    student_requests = StudentRequests.objects.raw(f"select id,school_id, status, student_id, request_date from request_studentrequests where status = 'Pending Approval' and request_date <= '{date.today()}' and school_id='{school_id.hex}' ")
    school_request = SchoolRequests.objects.filter(school_id=school_id, status="Pending Approval")
    context = {}
    
    context["student_requests"] = student_requests
    context["school_request"] = school_request
    context["school_id"] = school_id
    return render(request, "library/student_request_detail.html", context)



def calculate_date_with_days(date, days):
    return date + datetime.timedelta(days=days)


def approve_requests(request, school_id):
    #admin approve list of request form school and student
    if request.is_ajax:
        student_requests = StudentRequests.objects.filter(school_id=school_id, status="Pending Approval").update(status="Approved")
        school_request = SchoolRequests.objects.filter(school_id=school_id, status="Pending Approval").update(status="Approved")
        
    return JsonResponse({'data': "who are we"})

 

def approved_requests(request):
    """gets the approved requests of a particular school and it students"""
    student_requests = StudentRequests.objects.filter(school_id=request.user.school.school_id)
    school_request = SchoolRequests.objects.filter(school_id=request.user.school.school_id, status="Approved")

    data = []
    
    for book_request in student_requests:
        student = get_object_or_404(Student, student_id=book_request.student_id)
        book_request_data = {
            "id" : book_request.id,
            "book" : get_object_or_404(Book, id=book_request.book_id).title,
            "student" : student.name,
            "student_class" : student.school_class,
            "status" : book_request.status,
        }
        data.append(book_request_data)
    
    return JsonResponse({'data': data})
    




def school_all_requests(request):
    """gets the schools request for the school dashboard"""
    all_requests = SchoolRequests.objects.filter(school_id=request.user.school.school_id,)

    data = []
    for request in all_requests:
        school_request_data = {
            "id" : request.id,
            "book" : get_object_or_404(Book, id=request.book_id).title,
            "status" : request.status,
            "quantity" : request.quantity
        }
        data.append(school_request_data)

    return JsonResponse({'data': data})


def returned(request):
    pass