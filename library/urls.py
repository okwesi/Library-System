from django.contrib import admin
from django.urls import path,include, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

from django.conf import settings
admin.site.site_header = settings.ADMIN_SITE_HEADER
urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^$', views.home, name='home'),
    path("users/", include("users.urls")),
    path("user/", include("students_school.urls")),
    path("library/", include("library_app.urls")),
    path('books/', include("books.urls")),
    path('request/', include("request.urls")),
]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




