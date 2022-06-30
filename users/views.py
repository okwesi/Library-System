import random
from django.shortcuts import get_object_or_404, redirect, render

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import  Group
from django.contrib import messages
from library_app.forms import LibrarianForm
from library_app.models import Librarian, Library
from students_school.forms import StudentForm
from students_school.models import School, Student

# from users.models import Profile
# from . forms import EditUserForms, ProfileCreateForm, SignUpForm, PasswordChangeForms
from .forms import  CreateStudent, SignSchoolUpForm, SignUpForm, PasswordChangeForms

from django.contrib.auth import get_user_model

from django.utils.encoding import force_bytes, force_text
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
            # user.is_active = False
            # user.save()
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
            # # return render(request, 'try.html', {})
            return redirect('home')
    else:
        form = StudentForm()
    return render(request, 'registration/signup.html', {'form': form})



def signup_school(request):
    """function for creating forms to add users then sends a verification link to the email of the user"""
    print("open")
    if request.method == 'POST':
        print("post")
        form = SignSchoolUpForm(request.POST, auto_id="school_%s")
        # print(form.data)
        # print(form.errors)
        # print(form.non_field_errors)
        if form.is_valid():
            print("valid")
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
        form = SignSchoolUpForm()
    return render(request, 'librarian/signup_school.html', {'form': form})




def create_librarian(request):
    """function for creating forms to add users then sends a verification link to the email of the user"""
    if request.method == 'POST':
        form = LibrarianForm(request.POST)
        if form.is_valid():
            print(form.data)
            #save form in the memory not in database
            user = form.save()
            #adds a group to the user
            user_group = Group.objects.get(name='librarian')
            user.groups.add(user_group)

            Librarian.objects.create(
                user=user,
                full_name=form.cleaned_data.get("full_name"),
                library = request.user.librarian.library)

            current_site = get_current_site(request)
            mail_subject = 'Activation link has been sent to your email id'
            message = render_to_string('users/acc_active_email_librarians.html', {
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
            return redirect('home')
    else:
        form = LibrarianForm()
    return render(request, 'librarian/add_librarian.html', {'form': form})




def activate(request, uidb64, token):
    """function that activates the users account when they
    click on the activation link sent to their email"""
    User = get_user_model()
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'users/activate_success.html', {})
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