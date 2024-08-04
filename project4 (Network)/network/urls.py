
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("post", views.new_post, name="new_post"),
    path("like", views.likes, name="like"),
    path("profile/<str:name>", views.profile, name="profile"),
    path("follow/unfollow", views.follow_unfollow, name="follow/unfollow"),
    path("edit", views.edit, name="edit"),
    path("do_edit", views.do_edit, name="do_edit"),
    path("following", views.followings, name="following")
]
