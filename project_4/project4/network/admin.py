from django.contrib import admin
from .models import User, Like, Post, Follow

# Register your models here.
admin.site.register(User)
admin.site.register(Like)
admin.site.register(Post)
admin.site.register(Follow)
