from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    # email = forms.EmailField(widget= forms.EmailInput(attrs={'class': 'form-control'}), required=True)
    # phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder': ('Phone')}), label=("Phone number"), required=True)
    # password1 = forms.CharField(label='Password',widget= forms.PasswordInput(attrs={'class': 'form-control'}), required=True)
    # password2 = forms.CharField(label='Confirm Password',widget= forms.PasswordInput(attrs={'class': 'form-control'}), required=True)
    # full_name = forms.CharField(label="Full Name",max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    # library = forms.CharField()
   #the widget changes the default styling to to a bootstrap default form stylings
    class Meta:
        model = Book
        fields = ('title', 'about',  'stock',)
        
    
    
    
        
        
        