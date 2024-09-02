from django.shortcuts import render
from .models import Project, Course

# Create your views here.
def index(request):
    projects = Project.objects.all()
    '''projects = list(projects)
    project = projects[0]
    for _ in range(3):
        projects.append(project)'''
    return render(request, "projects/index.html", {
        "projects": projects
    })


def project_page(request, project_id):
    project = Project.objects.get(pk=int(project_id))

    return render(request, "projects/project_page.html", {
        "project": project
    })


def courses(request):
    courses = Course.objects.all()

    return render(request, "projects/courses.html", {
        "courses": courses
    })