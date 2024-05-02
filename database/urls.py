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
    path('<str:entity>/<int:ent_id>/', views.model_pages, name="model_page"),


    path('search_results/', project_views.search_results, name="search_results"),


    # path('add_new_records', views.add_new_records, name='add_new_records'),
    path('add_actor/', views.add_new_actor, name='add_actor'),
    path('add_campaign/', views.add_new_campaign, name='add_campaign'),
    path('add_publisher/', views.add_new_publisher, name='add_publisher'),
    path('add_system/', views.add_new_system, name='add_system'),
    path('add_producer/', views.add_new_producer, name='add_producer'),
    path('add_party/', views.add_new_party, name='add_party'),
    path('add_pc/', views.add_new_pc, name='add_pc'),
    path('add_episode/<int:campaign_id>', views.add_new_episode, name='add_episode'),

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
