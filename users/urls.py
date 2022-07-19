from django.urls.conf import path, include, re_path

from . views import *


urlpatterns = [
        path("accounts/login_user", login_user, name="login_user"),
        # url('signup/', UserSignUp.as_view(), name='signup'),
        path('accounts/signup/', signup_student, name='signup_student'),
        path('accounts/school-registration/', signup_school, name='signup_school'),
        path('accounts/librarian-registration/', create_librarian, name='create_librarian'),        
        path('accounts/', include('django.contrib.auth.urls')),
        re_path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',  activate, name='activate'),  
        # path('edit-usersettings/', UpdateUserDetails.as_view(), name='edit-usersettings'),
        path('librarian/update/', update_librarian, name='update-librarian'),
        path('school/update/', update_school, name='update-school'),
        path('student/update/', update_student, name='update-student'),
        
        
] 