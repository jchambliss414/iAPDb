from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landing_page),
    path('database/', include('database.urls')),
    path('members/', include('members.urls')),
    path('select2/', include('django_select2.urls')),


    path('elements', views.elements_test_page),
]
