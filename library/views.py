from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

def home(request):
    return render(request, 'home.html', {})


def hello_world(request):
    return JsonResponse({'text': "Hello World"})
