from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Categories, User, Listing, Watchlist, Bids, Comment


def index(request):
    return render(request, "auctions/index.html", {
        "active": Listing.objects.filter(close=False),
        "watchListCount": Watchlist.objects.filter(userId = request.user.id).count()
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
            endTime=endTime,
            userId = User.objects.get(pk = request.user.id)
        )
        create.save()
        messages.success(request, 'list have be success')
        return HttpResponseRedirect(reverse("index"))
        
        
    
    return render(request, "auctions/CreateList.html", {
        "Categories": Categories.objects.all(),
        "watchListCount": Watchlist.objects.filter(userId = request.user.id).count()
    })


def categories(request):

    if request.method == "POST":
        category = request.POST["category"]
        if category == "Category":
            return render(request, "auctions/category.html", {
                "EnterCategory": "Enter Catergory"
            })
        
        select = Listing.objects.filter(categoryID = Categories.objects.get(category=category), close=False)

        if not select:
            return render(request, "auctions/categoryPage.html", {
                "empty": "There is no list yet",
                "watchListCount": Watchlist.objects.filter(userId = request.user.id).count()
            })
        return render(request, "auctions/categoryPage.html", {
            "select": select,
            "watchListCount": Watchlist.objects.filter(userId = request.user.id).count()
        })

    return render(request, "auctions/category.html", {
        "Categories": Categories.objects.all(),
        "watchListCount": Watchlist.objects.filter(userId = request.user.id).count()
    })


def view(request, listing_id):
    view = Listing.objects.get(pk = listing_id)
    count = Bids.objects.filter(listId = listing_id).count()
    return render(request, "auctions/view.html",{
        "list" : view,
        "count": count,
        "watchListCount": Watchlist.objects.filter(userId = request.user.id).count()
    })

def addwatchlist(request, listing_id):
    if Watchlist.objects.filter(listId=listing_id, userId=request.user.id):
        messages.warning(request, 'This list Already in WatchList')
        return HttpResponseRedirect(reverse("index"))

    listing = Listing.objects.get(pk = listing_id)
    addwatchlist = Watchlist.objects.create(
        title=listing.title,
        discription=listing.discription,
        bid=listing.bid,
        urlImage=listing.urlImage,
        categoryID=listing.categoryID,
        startTime=listing.startTime,
        endTime=listing.endTime,
        userId = User.objects.get(pk = request.user.id),
        listId = Listing.objects.get(pk=listing_id),
        created_at = listing.created_at,
    ) 
    addwatchlist.save()
    messages.success(request, 'Added Successfully')
    return HttpResponseRedirect(reverse("watchlist"))

def watchlist(request):
    return render(request, "auctions/watchlist.html", {
        "watchlist" : Watchlist.objects.filter(userId = request.user.id),
        "watchListCount": Watchlist.objects.filter(userId = request.user.id).count()

    })


def delete(request, delete_id):
    if request.method == "POST":
        delete = Watchlist.objects.get(pk = delete_id, userId = request.user.id)
        delete.delete()
        messages.success(request, 'have been deleted successfully')
        return HttpResponseRedirect(reverse("watchlist"))


def bids(request, listing_id):
    if request.method == "POST":
        bid = int(request.POST["bid"])
        bids = Listing.objects.get(pk = listing_id)
        if bid <= bids.bid:
            messages.warning(request, 'bid must be greater than old price')
            return HttpResponseRedirect(reverse("view", args=(listing_id,)))
        bids.bid = bid
        bids.save()

        createBid = Bids.objects.create(
            bid = bids.bid,
            listId = Listing.objects.get(pk=bids.id),
            userId = User.objects.get(pk = request.user.id)
        )
        createBid.save()
        messages.success(request, 'success')
        
        return HttpResponseRedirect(reverse("view", args=(listing_id,)))


def comment(request, listing_id):
    if request.method == "POST":
        comment = request.POST["comment"]
    

        addcomment = Comment.objects.create(
            comment = comment,
            userId = User.objects.get(pk = request.user.id),
            listId = Listing.objects.get(pk=listing_id),
        ) 
        addcomment.save()
        return HttpResponseRedirect(reverse("comment", args=(listing_id,)))

    return render(request, "auctions/comment.html", {
        "comment": Listing.objects.get(pk = listing_id),
        "selectComment": Comment.objects.filter(listId = listing_id),
        "watchListCount": Watchlist.objects.filter(userId = request.user.id).count()
    })

def end(request, listing_id):
    list = Listing.objects.get(pk = listing_id)

    bid = Bids.objects.all()
    if not Bids.objects.filter(listId = listing_id, bid=list.bid).first() in bid:
        list.close = True
        list.save()
        messages.success(request, 'No winner')
        return HttpResponseRedirect(reverse("winner"))
        
    winnerName = Bids.objects.get(listId = listing_id, bid=list.bid)
    list.close = True
    list.winner = User.objects.get(pk= winnerName.userId.id)
    list.save()
    messages.success(request, 'check the winner')
    return HttpResponseRedirect(reverse("winner"))

def winner(request):
    return render(request, "auctions/winner.html", {
        "winners": Listing.objects.filter(close=True),
        "watchListCount": Watchlist.objects.filter(userId = request.user.id).count()
    })



