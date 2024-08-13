from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("sam", views.sam, name="sam"),
    path("<str:name>", views.greet, name="greet")
]
