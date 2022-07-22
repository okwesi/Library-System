from django import forms
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm, UserCreationForm
from library_app.models import Librarian
from users.models import User


class LibrarianForm(UserCreationForm):
    email = forms.EmailField(widget= forms.EmailInput(attrs={'class': 'form-control'}), required=True)
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder': ('Phone')}), required=True)
    password1 = forms.CharField(label='Password',widget= forms.PasswordInput(attrs={'class': 'form-control'}), required=True)
    password2 = forms.CharField(label='Confirm Password',widget= forms.PasswordInput(attrs={'class': 'form-control'}), required=True)
    full_name = forms.CharField(label="Full Name",max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    # library = forms.CharField()
   #the widget changes the default styling to to a bootstrap default form stylings
    class Meta:
        model = User
        fields = ('email', 'phone', 'password1', 'password2', "full_name" )
        







        
        
