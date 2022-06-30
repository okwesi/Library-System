from telnetlib import STATUS
from django.db import models
from books.models import Book
from students_school.models import School, Student

from users.models import User

# Create your models here.
class StudentRequests(models.Model):
    
    STATUS = (
        ('Pending Approval', 'Pending Approval'),
        ("Approved", "Approved"),
        ("Delivered", "Delivered"),
        ("Returned", "Returned")
    )
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    request_date = models.DateField(auto_now_add=True)
    returned_date = models.DateField(null=True, blank=True)
    quantity = models.IntegerField(default=1)
    status = models.CharField(max_length=200, choices=STATUS)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    
    
    
    
    
class SchoolRequests(models.Model):
    
    STATUS = (
        ('Pending Approval', 'Pending Approval'),
        ("Approved", "Approved"),
        ("Delivered", "Delivered"),
        ("Returned", "Returned")
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    request_date = models.DateField(auto_now_add=True)
    returned_date = models.DateField(null=True, blank=True)
    quantity = models.IntegerField()
    status = models.CharField(max_length=200, choices=STATUS)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    
    
    