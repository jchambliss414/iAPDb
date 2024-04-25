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
import iAPdb_Project.views as project_views

urlpatterns = [
    path('', views.database_home),
    path('campaigns/', views.campaign_database),
    path('actors/', views.actor_database),
    path('pcs/', views.pc_database),
    path('parties/', views.party_database),
    path('producers/', views.producer_database),
    path('systems/', views.system_database),
    path('publishers/', views.publisher_database),


    path('search_results/', project_views.search_results, name="search_results"),


    path('<str:entity>/<int:ent_id>/', views.model_pages, name="model_page"),


]
