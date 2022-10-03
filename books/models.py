
import uuid
from django.db import models

from library_app.models import Library

# Create your models here.



class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="Category")
    library = models.ForeignKey(Library, on_delete=models.CASCADE)


    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"{self.name}"
    


class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, auto_created=True)
    title = models.CharField(verbose_name="Title", max_length=200)
    about = models.TextField(verbose_name="About Book", max_length=1000)
    library = models.ForeignKey(Library, on_delete=models.CASCADE)
    stock = models.IntegerField(verbose_name="book quantity", null=False)
    book_cover = models.ImageField(upload_to='books/')
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    def __str__(self):
        return self.title




class NewBooks(models.Model):
    name = models.CharField(max_length=250)
    time_created = models.DateTimeField(auto_now=True, auto_now_add=False)
    library = models.ForeignKey(Library, on_delete=models.CASCADE)





