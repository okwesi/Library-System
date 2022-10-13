from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from request.models import StudentRequests

from users.models import User

def home(request):
    users = User.objects.all().order_by("email")
    books = StudentRequests.objects.raw(f"select  *, count(*) as number from request_studentrequests join books_book on request_studentrequests.book_id=books_book.id group by request_studentrequests.book_id  order by number desc")
   
    return render(request, 'home.html', {"users":users, "books":books})


def hello_world(request):
    return JsonResponse({'text': "Hello World"})
