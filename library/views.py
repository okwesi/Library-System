from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from users.models import User

def home(request):
    users = User.objects.all().order_by("email")
    return render(request, 'home.html', {"users":users})


def hello_world(request):
    return JsonResponse({'text': "Hello World"})
