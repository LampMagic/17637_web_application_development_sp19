from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
	path('', views.upload_action, name='home'),

    path('login', views.login_action, name='login'),
    path('logout', views.logout_action, name='logout'),
    path('register', views.register_action, name='register'),
    path('profile', views.profile_action, name='profile'),
    path('society', views.society_action, name='society'),
    path('other_user/<int:id>', views.other_user_action, name='other_user'),

    path('free_upload', views.free_upload_action, name='free_upload'),
    path('free_edit/<int:id>', views.free_edit_action, name='free_edit'),

    path('send_email/<int:id>', views.send_email, name='send_email'),
    path('upload_photo', views.upload_action, name='upload_photo'),
    path('edit_photo/<int:id>', views.edit_action, name='edit_photo'),
    path('tag/<int:id>', views.tag_action, name='tag'),
    path('get_photo/<int:id>', views.get_photo, name='get_photo'),
    path('save_photo/<int:id>', views.save_photo, name='save_photo'),
    path('delete_photo/<int:id>', views.delete_photo, name='delete_photo'),
    path('publish_photo/<int:id>', views.publish_photo, name='publish_photo'),
    path('photo_detail/<int:id>', views.photo_detail, name='photo_detail'),
]
