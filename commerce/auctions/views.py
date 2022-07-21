import re
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Categories, User, Listing


def index(request):
    return render(request, "auctions/index.html", {
        "active": Listing.objects.all()
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def CreateList(request):
    if request.method == "POST":
        title = request.POST["title"]
        discription = request.POST["discription"]
        bid = request.POST["bid"]
        urlImage = request.POST["image"]
        category = request.POST["category"]
        startTime = request.POST["startTime"]
        endTime = request.POST["endTime"]

        if not title or not discription or not bid or not urlImage or not startTime or not endTime:
            return render(request, "auctions/CreateList.html", {
                "title": "enter title",
                "dis": "add description",
                "bid": "enter price",
                "url": "enter url",
                "category": "enter category",
                "start": "enter start Time",
                "end": "enter end Time"
            })  
            
        create = Listing.objects.create(
            title=title,
            discription=discription,
            bid=bid,
            urlImage=urlImage,
            categoryID=Categories.objects.get(category=category),
            startTime=startTime,
            endTime=endTime
        )
        create.save()
        return HttpResponseRedirect(reverse("index"))
    
    return render(request, "auctions/CreateList.html", {
        "Categories": Categories.objects.all()
    })


def categories(request):

    if request.method == "POST":
        category = request.POST["category"]

        if category == "Category":
            return render(request, "auctions/category.html", {
                "EnterCategory": "Enter Catergory"
            })

        select = Listing.objects.filter(categoryID = Categories.objects.get(category=category))
        return render(request, "auctions/categoryPage.html", {
            "select": select
        })

    return render(request, "auctions/category.html", {
        "Categories": Categories.objects.all()
    })