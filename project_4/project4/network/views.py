from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import json
from django.http import JsonResponse
from django.db.utils import DataError
from django.core.paginator import Paginator

from .models import User, Post, Follow, Like


def index(request):
    if request.user.is_authenticated:
        bool = "true"
    else:
        bool = "false"

    posts = Post.objects.all()
    post_sorted_list = sorted(posts, key=lambda post: post.timestamp, reverse=True)
    pageinator = Paginator(post_sorted_list, 10)
    page_number = request.GET.get("page")
    post_list = pageinator.get_page(page_number)
    return render(request, "network/index.html", {
        "posts": post_list, "category": "All Posts",
        "bool": bool,
    })


def load_profile(request):
    if request.user.is_authenticated:
        bool = "true"
    else:
        bool = "false"
    
    user_id = request.GET.get("user_id")
    user = User.objects.get(pk=int(user_id))

    posts = user.user_posts.all()
    post_sorted_list = sorted(posts, key=lambda post: post.timestamp, reverse=True)
    pageinator = Paginator(post_sorted_list, 10)
    page_number = request.GET.get("page")
    post_list = pageinator.get_page(page_number)

    return render(request, "network/profile.html", {
        "profile_user": user, "user_posts": post_list,
        "bool": bool
    })


def following_page(request):
    if request.user.is_authenticated:
        bool = "true"
    else:
        bool = "false"

    user_id = request.user.id
    user = User.objects.get(pk=user_id)
    follow_objects = Follow.objects.filter(following_user=user)
    followed_users = [follow.followed_user for follow in follow_objects]

    posts = Post.objects.filter(user__in=followed_users)
    post_sorted_list = sorted(posts, key=lambda post: post.timestamp, reverse=True)
    pageinator = Paginator(post_sorted_list, 10)
    page_number = request.GET.get("page")
    post_list = pageinator.get_page(page_number)

    return render(request, "network/index.html", {
        "posts": post_list, "category": "Posts from followed users",
        "bool": bool,
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
    

def new_post(request):

    if request.method == "POST":
        data = json.loads(request.body)

        post_content = data.get("post_content", "")
        if post_content == "":
            return JsonResponse({"error": "Post body cannot be empty"}, status=201)
        
        user_id = data.get("post_user", "")
        user = User.objects.get(pk=user_id)

        try:
            post = Post(user=user, content=post_content)
            post.save()
        except DataError:
            return JsonResponse({"error": "Post is over the character limit"}, status=201)
        
        return JsonResponse({"error": ""}, status=201)
    

def edit_post(request):
    if request.method == "POST":
        data = json.loads(request.body)

        post_content = data.get("post_content", "")
        if post_content == "":
            return JsonResponse({"error": "Post body cannot be empty"}, status=201)
        
        post_id = data.get("post_id", "")
        post = Post.objects.get(pk=post_id)
        try:
            post.content = post_content
            post.save()
        except DataError:
            return JsonResponse({"error": "Post is over the character limit"}, status=201)
        
        return JsonResponse({"error": ""}, status=201)


def handle_like(request):
    if request.method == "POST":
        data = json.loads(request.body)
        post_id = data.get("post_id", "")
        action = data.get("action", "")
        print(f"post_id: {post_id}")

        user_id = request.user.id
        user = User.objects.get(pk=user_id)
        post = Post.objects.get(pk=post_id)

        if action == "add":
            like = Like(user=user, post=post)
            like.save()

            return JsonResponse({"status": "success"}, status=201)

        elif action == "remove":
            like = Like.objects.get(user=user, post=post)
            like.delete()

            return JsonResponse({"status": "success"}, status=201)
        else:
             return JsonResponse({"status": "fail"}, status=201)


    if request.user.is_authenticated: 
        post_ids = request.GET.get("post_id_list")
        post_id_list = post_ids.split(',')
        user_id = request.user.id

        json_response = {}

        user = User.objects.get(pk=user_id)
        for id in post_id_list:
            try:
                post = Post.objects.get(pk=int(id))
                Like.objects.get(post=post, user=user)
                json_response[id] = "true"
            except Like.DoesNotExist:
                json_response[id] = "false"
        
        return JsonResponse(json_response, status=200)


def handle_follow(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            data = json.loads(request.body)

            profile_user_id = data.get("profile_user", "")
            action = data.get("action", "")
            user_id = request.user.id

            active_user = User.objects.get(pk=user_id)
            profile_user = User.objects.get(pk=profile_user_id)

            if action == "follow":
                follow = Follow(followed_user=profile_user, following_user=active_user)
                follow.save()

                return JsonResponse({"status": "success"}, status=201)
            
            elif action == "unfollow":
                follow = Follow.objects.get(followed_user=profile_user, following_user=active_user)
                follow.delete()

                return JsonResponse({"status": "success"}, status=201)
        
        user_id = request.user.id
        target_user_id = request.GET.get("profile_user_id")
        
        active_user = User.objects.get(pk=user_id)
        profile_user = User.objects.get(pk=target_user_id)

        try:
            Follow.objects.get(followed_user=profile_user, following_user=active_user)
            bool = "true"
        except Follow.DoesNotExist:
            bool = "false"
        
        return JsonResponse({"following": bool}, status=200)