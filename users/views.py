import random
from django.shortcuts import get_object_or_404, redirect, render

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import  Group
from .models import User as passwordgen
# from django.contrib.auth import  User
from django.contrib import messages
from library_app.forms import LibrarianForm
from library_app.models import Librarian, Library
from students_school.forms import StudentForm, UpdateStudentForm
from students_school.models import School, Student

# from users.models import Profile
from . forms import EditUserForms, PasswordChangeForms, UpdateLibrarianForm, UpdateSchoolForm
from .forms import   SignSchoolUpForm, SignUpForm, PasswordChangeForms
from django.contrib.auth.views import PasswordChangeView
from django.views.generic.edit import UpdateView

from django.contrib.auth import get_user_model

from django.utils.encoding import force_bytes,force_str
from .tokens import account_activation_token

from django.core.mail import EmailMessage, send_mail

from django.http import HttpResponse

# """function for creating forms to add users then sends a verification link to the email of the user"""
#     if request.method == 'POST':
#         first_name = request.POST['first_name']
#         last_name = request.POST['last_name']
#         username = request.POST['username']
#         email = request.POST['email']
#         password = request.POST['password']
#         confirm_password = request.POST['confirm_password']

#         if password==confirm_password:
#             if User.objects.filter(username=username).exists():
#                 messages.info(request, 'Username is already taken')
#                 return redirect(createLibrarian)
#             elif User.objects.filter(email=email).exists():
#                 messages.info(request, 'Email is already taken')
#                 return redirect(createLibrarian)
#             else:
#                 user = User.objects.create_user(username=username, password=password, 
#                                         email=email, first_name=first_name, last_name=last_name)
#                 user.save()

#                 # to get the domain of the current site  
#                 current_site = get_current_site(request)  
#                 mail_subject = 'Activation link has been sent to your email id'  
#                 message = render_to_string('acc_active_email.html', {  
#                     'user': user,  
#                     'domain': current_site.domain, 
#                     "user_password" :  password,

#                 })  
#                 to_email = email 
#                 email = EmailMessage(  
#                             mail_subject, message, to=[to_email]  
#                 )  
#                 email.send()  
#                 return redirect('home')
#         else:
#             messages.info(request, 'Both passwords are not matching')
#             return redirect(createLibrarian)
#     else:
#         return render(request, 'signup.html')
def signup_student(request):
    """function for creating forms to add users then sends a verification link to the email of the user"""
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():            
            # save form in the memory not in database
            school = School.objects.get(school_number=form.cleaned_data.get("school_number"))
            # print(request.user.librarian.library)
            user = form.save()
            # email = form.cleaned_data.get("email"),
            # password1 = form.cleaned_data.get("password1")
            # password2 = form.cleaned_data.get("password2")
            user.is_active = False
            user.save()
            #adds a group to the user
            user_group = Group.objects.get(name='student')
            user.groups.add(user_group)
            #logs the user in after saving the user


            Student.objects.create(
                user=user,
                name = form.cleaned_data.get("name"),
                school = School.objects.get(school_id=school.school_id),
                city = form.cleaned_data.get("city"),
                address = form.cleaned_data.get("address"),
                gps_location = form.cleaned_data.get("gps_location"),
                school_class = form.cleaned_data.get("school_class"),
                )

            current_site = get_current_site(request)
            mail_subject = 'Activation link has been sent to your email id'
            message = render_to_string('users/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            messages.info(request, "Validate your registration in your email")
            return redirect('home')
    else:
        form = StudentForm()
    return render(request, 'registration/signup.html', {'form': form})



def signup_school(request):
    """function for creating forms to add users then sends a verification link to the email of the user"""
    if request.method == 'POST':
        form = SignSchoolUpForm(request.POST, auto_id="school_%s")
        print("save1")
        if form.is_valid():
            print(form)
            # save form in the memory not in database
            user = form.save()
            #adds a group to the user
            user_group = Group.objects.get(name='school')
            user.groups.add(user_group)


            School.objects.create(
                user = user,
                name = form.cleaned_data.get('name'),
                locations = form.cleaned_data.get('locations'),
                gps_location = form.cleaned_data.get('gps_location'),
                school_number = "SCH-"+str(random.randint(5600,100000)),
                library = request.user.librarian.library
            )
            #user.is_active = False

            current_site = get_current_site(request)
            mail_subject = 'Activation link has been sent to your email id'
            message = render_to_string('users/acc_active_email_school.html', {
                'user': user,
                'domain': current_site.domain,
                "user_password" :  form.cleaned_data.get('password1')
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            # return render(request, 'try.html', {})
            messages.success(request, f"{form.cleaned_data.get('name')} has been created")
            return redirect('get-schools')

    else:
        form = SignSchoolUpForm(auto_id="school_%s")
        password = passwordgen.objects.make_random_password()
    # messages.success(request, f"{form.error} has been created")
    return render(request, 'librarian/signup_school.html', {'form': form, "password":password})




def create_librarian(request):
    """function for creating forms to add users then sends a verification link to the email of the user"""
    if request.method == 'POST':
        form = LibrarianForm(request.POST)
        if form.is_valid():
            # print(form.data)
            #save form in the memory not in database
            # email = form.cleaned_data.get("email")
            # phone = form.cleaned_data.get("phone")
            # user = User.objects.create(email=email, password=password, phone=phone)

            user = form.save()
            #adds a group to the user
            user_group = Group.objects.get(name='librarian')
            user.groups.add(user_group)

            Librarian.objects.create(
                user=user,
                full_name=form.cleaned_data.get("full_name"),
                library = request.user.librarian.library)

            current_site = get_current_site(request)
            mail_subject = 'Email and passowrd'
            message = render_to_string('users/acc_active_email_librarians.html', {
                'user': user,
                'domain': current_site.domain,
                "user_password" :  form.cleaned_data.get("password1")
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            # return render(request, 'try.html', {})
            return redirect('query-librarians')
    else:
        form = LibrarianForm()
        password = passwordgen.objects.make_random_password()
            
    return render(request, 'librarian/add_librarian.html', {'form': form, "password":password})




def activate(request, uidb64, token):
    """function that activates the users account when they
    click on the activation link sent to their email"""
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Registration Validated, Please Login")
        return redirect("home")
        # return(request, 'home.html', {})
    else:
        return HttpResponse('Activation link is invalid!')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(email=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Invalid Email or Password')
            return redirect('login_user')

    else:
        return render(request, 'registration/login.html')
    
    
    
class UpdateUserDetails(UpdateView):
    """creates forms and allow users to update their details"""
    form_class = EditUserForms
    template_name = "users/updateuser.html"
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user


class PasswordChange(PasswordChangeView):
    """class for creating forms for users to change their passwords....
    currently not in use since this class is also provided by the allauth model"""
    form_class = PasswordChangeForms
    template_name = 'registration/password_change_form.html'
    def get_success_url(self, request):
        if request.user.groups.filter(name='student').exists():
            return reverse_lazy("get_books")
        elif request.user.groups.filter(name='school').exists():
            return reverse_lazy("school-dashboard")
        elif request.user.groups.filter(name='librarian').exists() or request.user.groups.filter(name='super librarian').exists():
            return reverse_lazy("school-dashboard")
        
        
def update_librarian(request):
    user = request.user
    librarian = request.user.librarian
    user_form = EditUserForms(instance=user)
    librarian_form = UpdateLibrarianForm(instance=librarian)
    if request.method == "POST":
        user_form = EditUserForms(request.POST,instance=user)
        librarian_form = UpdateLibrarianForm(request.POST, instance=librarian) 
        if user_form.is_valid() and librarian_form.is_valid():
            # user = user_form()
            # user.email = user_form.cleaned_data.get("email")
            # user.phone = user_form.cleaned_data.get("phone")
            user_form.save()
            librarian_form.save()
    context = {
        "user_form" : user_form,
        "librarian_form" : librarian_form
    }
    
    return render(request, "users/update/librarian.html", context)
    

def update_school(request):
    user = request.user
    school = request.user.school
    user_form = EditUserForms(instance=user)
    school_form = UpdateSchoolForm(instance=school)
    if request.method == "POST":
        user_form = EditUserForms(request.POST,instance=user)
        school_form = UpdateSchoolForm(request.POST, instance=school) 
        if user_form.is_valid() and school_form.is_valid():
            user_form.save()
            school_form.save()
    context = {
        "user_form" : user_form,
        "school_form" : school_form
    }
    
    return render(request, "users/update/school.html", context)




def update_student(request):
    user = request.user
    student = request.user.student
    user_form = EditUserForms(instance=user)
    student_form = UpdateStudentForm(instance=student)
    if request.method == "POST":
        user_form = EditUserForms(request.POST,instance=user)
        student_form = UpdateStudentForm(request.POST, instance=student) 
        if user_form.is_valid() and student_form.is_valid():
            user_form.save()
            student_form.save()
    context = {
        "user_form" : user_form,
        "student_form" : student_form
    }
    
    return render(request, "users/update/student.html", context)

