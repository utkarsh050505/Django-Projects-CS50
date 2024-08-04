from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:topic>", views.topic, name="topic"),
    path("search", views.search, name="search"),
    path("NewPage", views.create, name="create"),
    path("edit", views.edit, name="edit"),
    path("save", views.save, name="save"),
    path("random", views.random_topic, name="random_topic")
]
