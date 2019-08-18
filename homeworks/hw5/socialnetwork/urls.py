from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.global_stream_action, name='home'),
    path('login', views.login_action, name='login'),
    path('logout', views.logout_action, name='logout'),
    path('register', views.register_action, name='register'),

    path('global_stream', views.global_stream_action, name='global_stream'),
    path('follower_stream', views.follower_stream_action, name='follower_stream'),
    path('profile', views.profile_action, name='profile'),
    path('follower/<int:id>', views.follower_action, name='follower'),
    path('get_photo/<int:id>', views.get_photo, name='get_photo'),
]

