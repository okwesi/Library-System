from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm, UserCreationForm
from library_app.models import Library

from students_school.models import Student,School

from .models import User


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('email',  'phone', 'password')

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserCreationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',  'phone', 'is_staff', 'is_superuser')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(UserChangeForm):
    password = ReadOnlyPasswordHashField(label= ("Password"),
            help_text= ("Raw passwords are not stored, so there is no way to see "
                        "this user's password, but you can change the password "
                        "using <a href=\"../password/\">this form</a>."))
    class Meta:
        model = User
        fields = ('email', 'phone',  'password', 'is_active', 'is_superuser')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]
    


class SignUpForm(UserCreationForm):
    email = forms.EmailField(widget= forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password',widget= forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password',widget= forms.PasswordInput(attrs={'class': 'form-control'}))
    # name = forms.CharField(label="Student Name",max_length=100, widget=forms.TextInput())
    # location = forms.CharField(label="Student location",max_length=100, widget=forms.TextInput())
    # school = forms.CharField(label="Student location",max_length=100, widget=forms.TextInput())
    # school = forms.ModelChoiceField(queryset=School, to_field_name="name")

    
   #the widget changes the default styling to to a bootstrap default form stylings
    class Meta:
        model = User
        fields = ('email', 'phone', 'password1', 'password2', "phone")
# "name", "location", "school"

class CreateStudent(UserCreationForm):
    class Meta: 
        model: Student
        fields = ("name", "location")
        
        
class PasswordChangeForms(PasswordChangeForm):
    old_password = forms.CharField(label='Password', widget=forms.PasswordInput)
    new_password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    new_password2 = forms.CharField(label='Password', widget=forms.PasswordInput)

    
    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')


class SignSchoolUpForm(UserCreationForm):
    email = forms.EmailField(widget= forms.EmailInput(attrs={'class': 'form-control text-warning'}))
    # phone = forms.EmailField(widget= forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password',widget= forms.PasswordInput(attrs={'class': 'form-control text-warning'}))
    password2 = forms.CharField(label='Confirm Password',widget= forms.PasswordInput(attrs={'class': 'form-control text-warning'}))
    name = forms.CharField(label="School Name",max_length=100, widget=forms.TextInput(attrs={'class': 'form-control text-warning'}))
    locations = forms.CharField(label="School location",max_length=100, widget=forms.TextInput(attrs={'class': 'form-control text-warning'}))
    gps_location = forms.CharField(label="Digital Address", max_length=60, widget=forms.TextInput(attrs={'class': 'form-control text-warning'}))
    # library = forms. ModelChoiceField(queryset=Library.objects.all())
   #the widget changes the default styling to to a bootstrap default form stylings
    class Meta:
        model = User
        fields = ('email', 'phone', 'password1', 'password2',  "name", "locations", "gps_location")
# "name", "location", "school"
