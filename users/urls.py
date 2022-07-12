from django.conf.urls import url, include
from django.urls.conf import path

from . views import *


urlpatterns = [
        path("accounts/login_user", login_user, name="login_user"),
        # url('signup/', UserSignUp.as_view(), name='signup'),
        url('accounts/signup/', signup_student, name='signup_student'),
        url('accounts/school-registration/', signup_school, name='signup_school'),
        url('accounts/librarian-registration/', create_librarian, name='create_librarian'),        
        url('accounts/', include('django.contrib.auth.urls')),
        path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',  activate, name='activate'),  
        # url('edit-usersettings/', UpdateUserDetails.as_view(), name='edit-usersettings'),
        url('librarian/update/', update_librarian, name='update-librarian'),
        url('school/update/', update_school, name='update-school'),
        url('student/update/', update_student, name='update-student'),
        
        
] 