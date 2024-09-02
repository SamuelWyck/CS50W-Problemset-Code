from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("projects/project_page/<int:project_id>", views.project_page, name="project_page"),
    path("courses", views.courses, name="courses"),
]