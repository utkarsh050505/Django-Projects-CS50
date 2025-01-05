from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from .models import User, Listing, Category, Bids, Comments


def index(request):
    listing = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listing
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

@login_required
def create(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        return render(request, "auctions/create.html", {
            "category": categories
        })

    if request.method == 'POST':

        title = request.POST.get('title')
        description = request.POST.get('description')
        url = request.POST.get('ImageURL')
        price = request.POST.get('price')
        category = Category.objects.get(category_type=request.POST.get('type'))
        owner = User.objects.get(username=request.POST.get('user'))

        name_list = Listing(name=title, description=description, price=price, image=url, category=category, owner=owner)
        name_list.save()

        return redirect('index')

@login_required
def category(request):
    if request.method == 'GET':
        category_type = Category.objects.all()
        return render(request, "auctions/category.html", {
            "categories": category_type
        })

    elif request.method == 'POST':
        category_form = request.POST.get('category')
        category = Category.objects.get(category_type=category_form)
        list = Listing.objects.filter(active=True, category=category)
        return render(request, "auctions/index.html", {
            'listings': list,
            'message': f"Viewing in {category}"
        })


def id(request, id):

    listingData = Listing.objects.get(pk=id)
    isListinginWatchlist = request.user in listingData.watchlist.all()
    allComments = Comments.objects.filter(list=listingData)

    if request.method == 'GET':
        list = Listing.objects.get(pk=id)

        highest_bid = Bids.objects.filter(item=list).order_by('-highest_bid').first()

        if list.active == False:
            isInactive = True

            return render(request, "auctions/list.html", {
                'List': list,
                'isInactive': isInactive,
                'isListinginWatchlist': isListinginWatchlist,
                'Comments': allComments
            })

        if list.owner == request.user:
            isOwner = True

            return render(request, "auctions/list.html", {
                'List': list,
                'isListinginWatchlist': isListinginWatchlist,
                'isOwner': isOwner,
                'Bid': highest_bid,
                'Comments': allComments
            })



        if highest_bid and highest_bid.highest_bidder == request.user:
            return render(request, "auctions/list.html", {
                'List': list,
                "isListinginWatchlist": isListinginWatchlist,
                'message': ',Currently your bid is the highest bid',
                'Bid': highest_bid,
                'Comments': allComments
            })
        else:
            return render(request, "auctions/list.html", {
                'List': list,
                "isListinginWatchlist": isListinginWatchlist,
                'message': None,
                'Comments': allComments
            })

    elif request.method == 'POST':
        list = get_object_or_404(Listing, pk=id)
        amount = request.POST.get('bid_amount')

        amount = float(amount)

        if amount <= list.price:
            return render(request, "auctions/list.html", {
                'warning': 'Bid must be greater than the current price!',
                'List': list,
                'isListinginWatchlist': isListinginWatchlist,
                'Comments': allComments
            })

        highest_bidder = User.objects.get(username=request.POST.get('user'))
        current_highest_bid = Bids.objects.filter(item=list).order_by('-highest_bid').first()

        if current_highest_bid:
            # Update the existing bid
            current_highest_bid.highest_bid = amount
            current_highest_bid.highest_bidder = highest_bidder
            current_highest_bid.number_of_bid += 1
            current_highest_bid.save()
        else:
            # Create a new bid
            bid = Bids(item=list, highest_bidder=highest_bidder, highest_bid=amount, number_of_bid=1)
            bid.save()

        # Update the price of the listing
        list.price = amount
        list.save()

        return render(request, "auctions/list.html", {
            'List': list,
            "isListinginWatchlist": isListinginWatchlist,
            'Bid': current_highest_bid if current_highest_bid else bid,
            'Comments': allComments
        })


def addWatchlist(request, id):

    list = Listing.objects.get(pk=id)
    current_user = request.user
    list.watchlist.add(current_user)

    return HttpResponseRedirect(reverse('id', args=(id, )))

def removeWatchlist(request, id):

    list = Listing.objects.get(pk=id)
    current_user = request.user
    list.watchlist.remove(current_user)

    return HttpResponseRedirect(reverse('id', args=(id, )))

def watchlist(request):

    current_user = request.user
    listing = current_user.watch_list.all()

    return render(request, 'auctions/watchlist.html', {
        'listings': listing
    })

def close_auction(request, id):

    list = Listing.objects.get(pk=id)

    current_highest_bid = Bids.objects.filter(item=list).order_by('-highest_bid').first()

    list.active = False
    list.winner = current_highest_bid.highest_bidder
    list.save()

    return HttpResponseRedirect(reverse('id', args=(id, )))

def comments(request, id):

    list = Listing.objects.get(pk=id)

    newComment = Comments(comment=request.POST.get('comment'), list=list, user_commenting=request.user)
    newComment.save()

    return HttpResponseRedirect(reverse('id', args=(id, )))
