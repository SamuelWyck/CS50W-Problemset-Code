
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.new_post, name="new_post"),
    path("edit_post", views.edit_post, name="edit_post"),
    path("handle_like", views.handle_like, name="handle_like"),
    path("load_profile", views.load_profile, name="load_profile"),
    path("handle_follow", views.handle_follow, name="handle_follow"),
    path("following_page", views.following_page, name="following_page"),
]
