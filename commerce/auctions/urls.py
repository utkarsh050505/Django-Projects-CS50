from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("category", views.category, name="category"),
    path("listing/<int:id>", views.id, name="id"),
    path("addWatchlist/<int:id>", views.addWatchlist, name="addWatchlist"),
    path("removeWatchlist/<int:id>", views.removeWatchlist, name="removeWatchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("closeAuction/<int:id>", views.close_auction, name="closeAuction"),
    path("comments/<int:id>", views.comments, name="comments")
]
