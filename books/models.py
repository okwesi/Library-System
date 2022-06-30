from ast import mod
from enum import unique
import uuid
from django.db import models

from library_app.models import Library

# Create your models here.
class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, auto_created=True)
    title = models.CharField(verbose_name="Title", max_length=200)
    about = models.TextField(verbose_name="About Book", max_length=1000)
    library = models.ForeignKey(Library, on_delete=models.CASCADE)
    stock = models.IntegerField(verbose_name="book quantity", null=False)
    # image = models.ImageField(upload_to)
    def __str__(self):
        return self.title
    