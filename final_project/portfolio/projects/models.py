from django.db import models

# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=100, null=False)
    description = models.CharField(null=False, max_length=5000)
    languages_used = models.CharField(null=False, max_length=400)
    thumbnail = models.CharField(max_length=300, null=False, default="placeholder")
    video = models.CharField(max_length=200, null=False)
    code_link = models.CharField(max_length=200, default="placeholder")



#thumbnail = models.ImageField(null=False, upload_to="images/")

class Course(models.Model):
    title = models.CharField(max_length=200, null=False)
    description = models.CharField(max_length=5000, null=False)
    thumbnail = models.CharField(max_length=200, null=False, default="placeholder")
    code_link = models.CharField(max_length=200, default="placeholder")
    course_link = models.CharField(max_length=200, null=False)