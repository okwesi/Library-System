from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, get_user_model, password_validation
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm, UserCreationForm

from users.models import User
from .models import School, Student

class StudentForm(UserCreationForm):
   
    gender = (
        ('Gender', 'Gender'),
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    classes = (
        ('Choose class', 'Choose class'),
        ('JHS 1', 'JHS 1'),
        ('JHS 2', 'JHS 2'),
        ('JHS 3', 'JHS 3'),
        ('PRIMARY 6', 'PRIMARY 6'),
        ('PRIMARY 5', 'PRIMARY 5'),
        ('PRIMARY 4', 'PRIMARY 4'),
        ('PRIMARY 3', 'PRIMARY 3'),
        ('PRIMARY 2', 'PRIMARY 2'),
        ('PRIMARY 1', 'PRIMARY 1'),)
    
    email = forms.EmailField(widget= forms.EmailInput(attrs={'class': 'form-control text-warning rounded-pill', 'autocomplete': "off"}))
    password1 = forms.CharField(label='Password',widget= forms.PasswordInput(attrs={'class': 'form-control text-warning rounded-pill '}))
    password2 = forms.CharField(label='Confirm Password',widget= forms.PasswordInput(attrs={'class': 'form-control text-warning rounded-pill'}))
    name = forms.CharField(label="Student Name",max_length=100, widget=forms.TextInput(attrs={'class': 'form-control text-warning rounded-pill'}))
    school_number = forms.CharField(label="School",max_length=100, widget=forms.TextInput(attrs={'class': 'form-control text-warning rounded-pill'}))
    city = forms.CharField(label="City",max_length=100, widget=forms.TextInput(attrs={'class': 'form-control text-warning rounded-pill'}))
    address = forms.CharField(label="Address",max_length=100, widget=forms.TextInput(attrs={'class': 'form-control text-warning rounded-pill' }))
    gps_location = forms.CharField(label="Digital Address",max_length=100, widget=forms.TextInput(attrs={'class': 'form-control text-warning rounded-pill'}))
    school_class = forms.ChoiceField(choices=classes ,label="Class")
    # location = forms.CharField(label="Student location",max_length=100, widget=forms.TextInput())
    gender = forms.ChoiceField(choices=gender ,label="Gender")
    class Meta:
        model = User
        fields = (
           "email",
           "password1",
           "password2",
           "phone",
           "name",
           "school_number",
           "city",
           "address",
           "gender",
           "gps_location", 
           "school_class",
       )
       




class SchoolForm(forms.ModelForm):
    about = forms.CharField(label="About School",max_length=100, widget=forms.Textarea())

    class Meta:
        model = School
        fields = (
            'name',
            'about',
            'locations',
            'library',
            'gps_location',
        )
        


        
        
        
        
        
        
class UpdateStudentForm(forms.ModelForm):
   
    gender = (
        ('Gender', 'Gender'),
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    classes = (
        ('Choose class', 'Choose class'),
        ('JHS 1', 'JHS 1'),
        ('JHS 2', 'JHS 2'),
        ('JHS 3', 'JHS 3'),
        ('PRIMARY 6', 'PRIMARY 6'),
        ('PRIMARY 5', 'PRIMARY 5'),
        ('PRIMARY 4', 'PRIMARY 4'),
        ('PRIMARY 3', 'PRIMARY 3'),
        ('PRIMARY 2', 'PRIMARY 2'),
        ('PRIMARY 1', 'PRIMARY 1'),)
    
    name = forms.CharField(label="Student Name",max_length=100, widget=forms.TextInput(attrs={'class': 'form-control text-warning rounded-pill'}))
    school_number = forms.CharField(label="School",max_length=100, widget=forms.TextInput(attrs={'class': 'form-control text-warning rounded-pill'}))
    city = forms.CharField(label="City",max_length=100, widget=forms.TextInput(attrs={'class': 'form-control text-warning rounded-pill'}))
    address = forms.CharField(label="Address",max_length=100, widget=forms.TextInput(attrs={'class': 'form-control text-warning rounded-pill' }))
    gps_location = forms.CharField(label="Digital Address",max_length=100, widget=forms.TextInput(attrs={'class': 'form-control text-warning rounded-pill'}))
    school_class = forms.ChoiceField(choices=classes ,label="Class")
    # location = forms.CharField(label="Student location",max_length=100, widget=forms.TextInput())
    gender = forms.ChoiceField(choices=gender ,label="Gender")
    class Meta:
        model = Student
        fields = (
           "name",
           "school_number",
           "city",
           "address",
           "gender",
           "gps_location", 
           "school_class",
       )
