from django.urls import path, include
import members.views as views

urlpatterns = [
    path('', views.members_list),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register', views.register_user, name='register_user'),
    path('<int:user_id>', views.user_homepage, name='user_home'),
    path('<int:user_id>/inbox', views.inbox, name='inbox'),
    path('<int:user_id>/message/<int:notification_id>', views.read_notification, name='notification'),
    path('crud_event/<int:update_id>', views.read_crud_update, name='crud_update'),
]
