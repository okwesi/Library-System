from telnetlib import STATUS
from django.db import models
from books.models import Book
from library_app.models import Library
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
    library = models.ForeignKey(Library, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"student-{self.student.name} ----- book-{self.book.title}"
    
    
    
    
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
    library = models.ForeignKey(Library, on_delete=models.CASCADE, null=True, blank=True)
    
    
    