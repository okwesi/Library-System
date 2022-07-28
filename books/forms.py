from django import forms
from .models import Book, Category

class BookForm(forms.ModelForm):
    title = forms.CharField(label="Book Title",max_length=300, widget=forms.TextInput(attrs={'class': 'form-control text-warning'}), required=True)
    about = forms.Textarea()
    stock = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control text-warning'}))
    book_cover = forms.FileField(widget=forms.ClearableFileInput(attrs={"class":"form-control", "capture":"camera", "accept":"image/*"}))
    category = forms.ModelChoiceField(queryset=None)
   #the widget changes the default styling to to a bootstrap default form stylings
    class Meta:
        model = Book
        fields = ('title', 'about',   'stock', 'category','book_cover')
        
    

        
        
        