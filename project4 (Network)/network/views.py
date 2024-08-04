from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from datetime import datetime

from .models import User, Posts


def index(request):

    posts = Posts.objects.all()
    return render(request, "network/index.html", {
        "posts":reversed(posts)
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

    if request.method == 'POST':

        user = User.objects.get(username=request.POST.get('user'))
        content = request.POST.get('content')

        post = Posts(content=content, user_posting=user, likes=0)
        post.save()

        return redirect('index')

    else:
        return render(request, "network/new_post.html")

def likes(request):

    if request.method == 'POST':

        post = Posts.objects.get(pk=(request.POST.get("post_id")))

        user = User.objects.get(username=request.POST.get('user'))

        if post.user_liking.filter(id=user.id).exists():
                # Unlike
                post.likes -= 1
                post.user_liking.remove(user)
        else:
                # Like
                post.likes += 1
                post.user_liking.add(user)

        # Save the changes to the post
        post.save()

        return redirect("index")

    else:

        return redirect('index')

def profile(request, name):

    user = User.objects.get(username=name)

    return render(request, "network/profile.html", {
        'User': user
    })

def follow_unfollow(request):

    if request.method == 'POST':

        user = User.objects.get(username=request.POST.get('user_account'))
        person = User.objects.get(username=request.POST.get('person'))

        if person.followers.filter(id=user.id).exists():

            person.number_of_followers -= 1
            person.followers.remove(user)
            user.number_of_following -= 1
            user.following.remove(person)

        else:

            person.number_of_followers += 1
            person.followers.add(user)
            user.number_of_following += 1
            user.following.add(person)

        person.save()
        user.save()

        return HttpResponseRedirect(reverse('profile', args=(person.username, )))

def edit(request):

    if request.method == 'POST':

        text = request.POST.get('cont')
        edit = True
        id = request.POST.get('id')

        return render(request, "network/new_post.html", {
            "text": text,
            "edit": edit,
            "id": id
        })

def do_edit(request):

    if request.method == 'POST':

        id = request.POST.get('post_id')

        post = Posts.objects.get(id=id)

        post.content = request.POST.get('content')

        post.save()

        return redirect('index')

    else:

        return redirect('index')

def followings(request):

    user = User.objects.get(username=request.user.username)

    followin = user.following.all()

    posts = Posts.objects.filter(user_posting__in=followin).all()

    print(posts)

    return render(request, "network/index.html", {
        "posts": posts
    })
