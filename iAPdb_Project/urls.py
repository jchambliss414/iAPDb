from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landing_page),
    path('database/', include('database.urls')),
    path('members/', include('members.urls')),
    path('select2/', include('django_select2.urls')),


    path('elements', views.elements_test_page),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
