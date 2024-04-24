from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landing_page),
    path('database/', include('database.urls')),
    path('members/', include('members.urls')),


    path('elements', views.elements_test_page),
    path('campaign_test', views.campaign_model_test),
    path('actor_test', views.actor_model_test),
    path('pc_test', views.pc_model_test),
    path('party_test', views.party_model_test),
    path('producer_test', views.producer_model_test),
    path('system_test', views.system_model_test),
    path('publisher_test', views.publisher_model_test),
]
