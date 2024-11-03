from django.urls import path
from . import views


urlpatterns = [
  path('', views.home, name="home"),
  path('update_room/<str:pk>', views.update_room, name="update-room"),
  path('topic/', views.topic_view, name="topic-view"),
  path('activity/', views.activity_view, name="activity-view"),
  path('userInfo/<str:pk>', views.userInfo, name="userInfo"),
  path('editUser/<str:pk>', views.editUser, name="edit-user"),
  path('room/', views.room_form, name="room_form"),
  path('roomDetails/<str:pk>', views.roomDetails, name="room-details"),
  path('delete_room/<str:pk>', views.delete_room, name="delete-room"),
  path('delete_message/<str:pk>', views.delete_message, name="delete-message"),
  path('login/', views.login_view, name="login"),
  path('signup/', views.signup_view, name="signup"),
  path('logout/', views.logout_view, name="logout"),
  ]