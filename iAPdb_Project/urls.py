"""
URL configuration for iAPdb_Project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
import database

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landing_page),
    path('', views.landing_page),
    path('database/', include('database.urls')),


    path('elements', views.elements_test_page),
    path('campaign_test', views.campaign_model_test),
    path('actor_test', views.actor_model_test),
    path('pc_test', views.pc_model_test),
    path('party_test', views.party_model_test),
    path('producer_test', views.producer_model_test),
    path('system_test', views.system_model_test),
    path('publisher_test', views.publisher_model_test),
]
