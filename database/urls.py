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
    path('<str:entity>/', views.database_pages, name="database_page"),
    path('<str:entity>/<int:ent_id>', views.model_pages, name="model_page"),

    path('search_results/', project_views.search_results, name="search_results"),

    path('add_new_records', views.add_new_records, name='add_new_records'),
    path('add/<str:entity>/', views.add_new_model, name='add_model'),
    path('edit/<str:entity>/<int:ent_id>/', views.edit_model, name='edit_model'),
    path('campaigns/<int:campaign_id>/add_episode/', views.add_new_episode, name='add_episode'),

    # path('edit_producer/<int:producer_id>', views.edit_producer, name='edit_producer'),
    # path('edit_actor/<int:actor_id>', views.edit_actor, name='edit_actor'),
    # path('edit_campaign/<int:campaign_id>', views.edit_campaign, name='edit_campaign'),
    # path('edit_party/<int:party_id>', views.edit_party, name='edit_party'),
    # path('edit_episode/<int:episode_id>', views.edit_episode, name='edit_episode'),
    # path('edit_pc/<int:pc_id>', views.edit_pc, name='edit_pc'),
    # path('edit_publisher/<int:publisher_id>', views.edit_publisher, name='edit_publisher'),
    # path('edit_system/<int:system_id>', views.edit_system, name='edit_system'),
    #
    # path('manage_campaigns/producer/<int:producer_id>', views.manage_campaigns, name='manage_campaigns'),
    # path('manage_parties/campaign/<int:campaign_id>', views.manage_parties, name='manage_parties'),
    # path('manage_episodes/campaign/<int:campaign_id>', views.manage_episodes, name='manage_episodes'),




]
