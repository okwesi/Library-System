import datetime
from django.http import  JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from datetime import date


from books.models import Book
from request.forms import SchoolRequestForm
from request.models import SchoolRequests, StudentRequests
from students_school.models import School, Student

# Create your views here.

def student_request(request, book_id): 
    if request.method == "POST":
        user = request.user.student
        book = get_object_or_404(Book, id=book_id)
        school = request.user.student.school
        library = request.user.student.school.library
        if book.stock > 0:
            status = "Pending Approval";
            user.borrowed = True
            book.stock = book.stock - 1
            student_request = StudentRequests(student=user, book=book, status=status, school=school, library=library )
            student_request.save()  
            book.save()      
            user.save()
            return redirect("public-books")
        else:
            messages.error(request, "Book is unavailable")
            return redirect("book-detail", id=book_id)
        
    
    
#handles school request  for books
def school_request(request, book_id): 
    form = SchoolRequestForm(request.POST or None)
    # if request.method == "POST":
    if form.is_valid():
        print (form.cleaned_data.get("quantity"))
        requested_quantity = form.cleaned_data.get("quantity")
        user = request.user.school
        library = request.user.school.library
        user.borrowed = True
        # print(user)
        book = get_object_or_404(Book, id=book_id)
        if book.stock >= requested_quantity:
            book.stock = book.stock - requested_quantity
            status = "Pending Approval";
            quantity = requested_quantity
            
            school_request = SchoolRequests(school=user, book=book, status=status, quantity=quantity, library=library)
            school_request.save()        
            user.save()
            book.save()
            messages.success(request, "Book Requested successfully")
            return redirect("book-detail", id=book_id)
        else:
            request_form = SchoolRequestForm()   
            context = {
                "book" : book, 
                "request_form" : request_form       
            }
            messages.error(request, "Book Request unsuccessful, Quantity requested is more quantity at stock")
            return redirect("book-detail", id=book_id)
    
   
   
   
   
   
   
        
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


def librarian_requests(request):
    requests = StudentRequests.objects.raw(f"select id,school_id, request_date,  count(*) count from (select id,school_id, status, student_id, request_date from request_studentrequests where status = 'Pending Approval' and request_date <= '{date.today()}' and library_id='{request.user.librarian.library.id.hex}') group by school_id ")
    
    return render(request, 'librarian/request.html', {"requests":requests})

def librarian_received(request):
    requests = StudentRequests.objects.raw(f"select id,school_id, request_date,  count(*) count from (select id,school_id, status, student_id, request_date from request_studentrequests where status = 'Received' and library_id='{request.user.librarian.library.id.hex}' ) group by school_id ")
    return render(request, 'librarian/received.html', {"requests":requests})




def librarian_get_request_details(request, school_id):
    """gets book requests with Pending Approval status"""
    student_requests = StudentRequests.objects.raw(f"select id,school_id, status, student_id, request_date from request_studentrequests where status = 'Pending Approval' and request_date <= '{date.today()}' and school_id='{school_id.hex}' ")
    school_request = SchoolRequests.objects.filter(school_id=school_id, status="Pending Approval")
    context = {}
    
    context["student_requests"] = student_requests
    context["school_request"] = school_request
    context["school_id"] = school_id
    
    if request.method == "POST":
        student_requests = StudentRequests.objects.filter(school_id=school_id, status="Pending Approval").update(status="Approved")
        school_request = SchoolRequests.objects.filter(school_id=school_id, status="Pending Approval").update(status="Approved")   
        messages.success(request,  f"{get_object_or_404(School, school_id=school_id)}'s Request has been approved")
        return redirect("librarian_get_grouped_request")
    # else:
        # messages.error(request,  f"Something Went Wrong")    
        # # return render(request, "librarian/student_request_detail.html", context)
    return render(request, "librarian/student_request_detail.html", context)




def librarian_get_received_details(request, school_id):
    """gets book requests with Pending Approval status"""
    student_requests = StudentRequests.objects.raw(f"select id,school_id, status, student_id, request_date from request_studentrequests where status = 'Received' and school_id='{school_id.hex}' ")
    school_request = SchoolRequests.objects.filter(school_id=school_id, status="Received")
    context = {}
    
    context["student_requests"] = student_requests
    context["school_request"] = school_request
    context["school_id"] = school_id
    
    return render(request, "librarian/student_received_detail.html", context)





def calculate_date_with_days(date, days):
    return date + datetime.timedelta(days=days)


def approve_requests(request, school_id):
    #admin approve list of request form school and student
    if request.method == "POST":
        student_requests = StudentRequests.objects.filter(school_id=school_id, status="Pending Approval").update(status="Approved")
        school_request = SchoolRequests.objects.filter(school_id=school_id, status="Pending Approval").update(status="Approved")   
        messages.success(request,  f"{get_object_or_404(School, school_id=school_id)}'s Request has been approved")
        return redirect("librarian_get_grouped_request")
    else:
        messages.error(request,  f"Something Went Wrong")
        return
        

def return_requests(request, school_id):
    #admin approve list of request form school and student
    if request.method == "POST":
        student_requests = StudentRequests.objects.filter(school_id=school_id, status="Received")
        school_request = SchoolRequests.objects.filter(school_id=school_id, status="Received")   
    
        for request in student_requests:
            #TODO: increase the book quantity by one        
            request.book.stock = request.book.stock + 1
            #TODO: flag borrowed of user as false
            request.student.borrowed = False
            request.returned_date = date.today()
            request.book.save()
            request.student.save()
            request.save()
        
            
        for request in school_request:        
            #TODO: For school get the quantity and add it to the book stock
            request.book.stock = request.book.stock + request.quantity
            #TODO: flag the school borrowed as false
            request.school.borrowed = False
            request.returned_date = date.today()

            
            request.book.save()
            request.school.save()
            request.save()
        
        #TODO: flag all orders as returned        
        student_requests.update(status="Returned")
        school_request.update(status='Returned')   
        
        # messages.success(request, "Books have been Received😊")
        return redirect("librarian_get_grouped_received")
    
    return redirect("received-details", school_id=school_id)
    

# .update(status="Approved")








 

def School_requests(request):
    """gets the approved requests of a particular school and it students"""
    student_requests = StudentRequests.objects.filter(school_id=request.user.school.school_id, status="Pending Approval")
    school_request = SchoolRequests.objects.filter(school_id=request.user.school.school_id, status="Pending Approval").first()
    # get_object_or_404(SchoolRequests, school_id=request.user.school.school_id, status="Pending Approval")

    # data = []    
    # for book_request in student_requests:
    #     student = get_object_or_404(Student, student_id=book_request.student_id)
    #     book_request_data = {
    #         "id" : book_request.id,
    #         "book" : get_object_or_404(Book, id=book_request.book_id).title,
    #         "student" : student.name,
    #         "student_class" : student.school_class,
    #         "status" : book_request.status,
    #     }
    #     data.append(book_request_data)
    
    # return JsonResponse({'data': data})
    context = {
        "school_request" : school_request,
        "student_requests" : student_requests
    }

    return render(request, "school/order.html", context)
    



# nmi
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



def school_approved_requests(request):
    #admin set returned to book and requests
    student_requests = StudentRequests.objects.filter(school_id=request.user.school.school_id, status="Approved")
    school_request = SchoolRequests.objects.filter(school_id=request.user.school.school_id, status="Approved").first()
    context = {
        'student_requests' : student_requests, 
        "school_request" : school_request,
        "school_id" : request.user.school.school_id
    }
    return render(request, 'school/approved.html', context)




def School_set_received(request):
    if request.method == "POST":
        student_requests = StudentRequests.objects.filter(school_id=request.user.school.school_id, status="Approved").update(status="Received")
        school_request = SchoolRequests.objects.filter(school_id=request.user.school.school_id, status="Approved").update(status="Received")
        messages.success(request, "Books have been Received😊")
        return redirect('school_received_requests')
    else:
        messages.warning(request, "Something Went Wrong")
        return redirect('school_approved_requests')
    
    
    
def school_received_requests(request):
    #admin set returned to book and requests
    student_requests = StudentRequests.objects.filter(school_id=request.user.school.school_id, status="Received")
    school_request = SchoolRequests.objects.filter(school_id=request.user.school.school_id, status="Received").first()
    context = {
        'student_requests' : student_requests, 
        "school_request" : school_request,
        "school_id" : request.user.school.school_id
    }
    return render(request, 'school/received.html', context)






