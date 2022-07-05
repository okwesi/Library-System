from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

from django.conf import settings
admin.site.site_header = settings.ADMIN_SITE_HEADER
urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),
    url("users/", include("users.urls")),
    url("user/", include("students_school.urls")),
    url("library/", include("library_app.urls")),
    url('books/', include("books.urls")),
    url('request/', include("request.urls")),
]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




