import random
from tabnanny import verbose
from django.db import models
import uuid
from django.db.models.signals import post_save

from django.dispatch import receiver
from library_app.models import Library
from users.models import User


def generate_number():
    return "SCH-"+str(random.randint(5600,100000))
   
# Create your models here.
class  School(models.Model): 
    school_id = models.UUIDField(auto_created=True,default=uuid.uuid4, primary_key=True, unique=True)
    user = models.OneToOneField(User, verbose_name="School Account", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="school name", max_length=100, unique=True)
    locations = models.CharField(verbose_name="school location", max_length=100)
    library = models.ForeignKey(Library, on_delete=models.CASCADE)
    school_number = models.CharField(verbose_name="school number", max_length=10, unique=True, editable=False,default=generate_number, blank=True, null=True)
    gps_location = models.CharField(verbose_name="Ghana GPS", max_length=50)
    about_school = models.TextField(verbose_name="About", max_length=1000, null=True, blank=True)
    borrowed = models.BooleanField(default=False)
    def __str__(self):
        return self.name
    
 

    
    
    
    
    
# Profiles 
# Student 
Gender_Choices = (
        ('Gender', 'Gender'),
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
Class_Choices = (
        ('Choose', 'Choose'),
        ('JHS 1', 'JHS 1'),
        ('JHS 2', 'JHS 2'),
        ('JHS 3', 'JHS 3'),
        ('PRIMARY 6', 'PRIMARY 6'),
        ('PRIMARY 5', 'PRIMARY 5'),
        ('PRIMARY 4', 'PRIMARY 4'),
        ('PRIMARY 3', 'PRIMARY 3'),
        ('PRIMARY 2', 'PRIMARY 2'),
        ('PRIMARY 1', 'PRIMARY 1'),
        
    )
class Student(models.Model):
    student_id = models.UUIDField(auto_created=True, default=uuid.uuid4, unique=True, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(verbose_name="full Name",max_length=60)
    school = models.ForeignKey(School,verbose_name="school", on_delete=models.CASCADE)
    city = models.CharField(verbose_name="city", max_length=100)
    address = models.CharField(verbose_name="address", max_length=60)
    gps_location = models.CharField(verbose_name="ghana gps", max_length=60)
    school_class = models.CharField(verbose_name="Class", max_length=60, choices=Class_Choices, )
    gender = models.CharField(verbose_name="gender", max_length=10, choices=Gender_Choices,)
    borrowed = models.BooleanField(default=False)
    def __str__(self):
        return self.user.email

    # @receiver(post_save, sender=User)
    # def update_profile_signal(sender, instance, created, **kwargs):
    #     if created:
    #         Student.objects.create(user=instance)
    #     instance.student.save()