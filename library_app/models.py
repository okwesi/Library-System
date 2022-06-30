from tabnanny import verbose
from urllib import request
import uuid
from django.db import models
from ckeditor.fields import RichTextField
from django.dispatch import receiver
from django.db.models.signals import post_save

from users.models import User

# Create your models here.

class Library(models.Model):
    id = models.UUIDField(verbose_name="library id", default=uuid.uuid4, primary_key=True, auto_created=True, unique=True)
    name = models.CharField(verbose_name="library name", max_length=255, unique=True)
    location = models.CharField(verbose_name="library location", max_length=255, unique=True)
    about = RichTextField()
    gps_location = models.CharField(verbose_name="Ghana GPS", max_length=100)
    
    def __str__(self):
        return self.name
    
    
    class Meta:
        verbose_name = "library"
        verbose_name_plural = "libraries"
    
    
class Librarian(models.Model):
    id = models.UUIDField(verbose_name="librarian id", unique=True, default=uuid.uuid4, primary_key=True, auto_created=True)
    full_name = models.CharField(verbose_name="full name", max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    library = models.ForeignKey(Library, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.full_name
    
    
# @receiver(post_save, sender=User)
# def update_librarian_signal(sender, instance, created, **kwargs):
#     if created:
#         Librarian.objects.create(user=instance)
#     instance.librarian.save()