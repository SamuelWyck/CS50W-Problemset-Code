from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry_page, name="entry_page"),
    path("results/", views.results, name="results"),
    path("new_page/", views.new_page, name="new_page"),
    path("<str:entry>", views.edit_page, name="edit_page"),
    path("random_page/", views.get_random_page, name="random_page"),
]
