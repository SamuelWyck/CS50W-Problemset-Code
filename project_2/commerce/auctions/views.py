from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from .models import User, AuctionListings, Bid, Comments, WatchListedItem
CATEGORIES = [
('', 'Select Category'),
("1", "Collectibles & Art"),
("2", "Clothing, Shoes & Accessories"),
("3", "Sporting Goods"),
("4", "Electronics"),
("5", "Toys & Hobbies"),
("6", "Home & Garden"),
("7", "Games"),
("8", "Jewelry & Watches"),
("9", "Books, Movies & Music"),
("10", "Health & Beauty"),
("11", "Vehicles & Vehicle Parts"),
("12", "Pet Supplies"),
]

class NewListingForm(forms.Form):
    title = forms.CharField(label="Title", max_length=64, required=True)
    title.widget.attrs.update({"placeholder": "Title", "class": "form-control", "style": "width: 20%; margin-bottom: 20px;"})

    price = forms.DecimalField(max_digits=10, decimal_places=2, label="Starting Price", required=True)
    price.widget.attrs.update({"placeholder": "USD", "class": "form-control", "style": "width: 20%; margin-bottom: 20px;"})

    category = forms.ChoiceField(widget=forms.Select(), required=True, choices=CATEGORIES)
    category.widget.attrs.update({"class": "form-control", "style": "width: 20%; margin-bottom: 20px;"})

    image = forms.ImageField(label="Image URL", required=False)
    image.widget.attrs.update({"class": "form-control", "style": "width: 20%; margin-bottom: 20px;"})

    description = forms.CharField(max_length=200, label="Description", widget=forms.Textarea, required=True)
    description.widget.attrs.update({"class": "form-control", "placeholder": "Describe your listing", "style": "width: 40%; margin-bottom: 20px;"})


class NewBidForm(forms.Form):
    amount = forms.DecimalField(max_digits=20, decimal_places=2, label="")
    amount.widget.attrs.update({"placeholder": "Bid", "class": "form-control", "style": "margin: 5px;"})


class NewCommentForm(forms.Form):
    comment = forms.CharField(max_length=400, label="", widget=forms.Textarea, required=True)
    comment.widget.attrs.update({"placeholder": "Comment:", "class": "form-control", "rows": 5, "style": "width: 100%;"})


def index(request):
    return render(request, "auctions/index.html", {
        "listings": AuctionListings.objects.filter(active=True),
        "MEDIA_URL": settings.MEDIA_URL,
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
def create_listing(request):
    if request.method == "POST":
        form = NewListingForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data["title"]
            price = form.cleaned_data["price"]
            category_value = form.cleaned_data["category"]
            category = dict(form.fields['category'].choices)[category_value]
            image = form.cleaned_data["image"]
            description = form.cleaned_data["description"]
            seller = User.objects.get(pk=int(request.user.id))

            Listing = AuctionListings(
            name=title, starting_price=price, category=category, description=description, image=image, seller=seller)
            Listing.save()
            return HttpResponseRedirect(reverse('index'))
        
        else:
            return render(request, "auctions/create_listing.html", {
                "form": NewListingForm(), "message": "All fields must be properly filled"
            })
    
    return render(request, "auctions/create_listing.html", {
        "form": NewListingForm()
    })


def listing_page(request, listing_id, message=None):
   
    listing = AuctionListings.objects.get(pk=int(listing_id))
    comment_objects = listing.comments.all()
    if request.user.is_authenticated:
        user = User.objects.get(pk=int(request.user.id))
    else:
        user = None
    try:
        if user:
            watchlisted = user.watchlisted.get(listing=listing)
        else:
            watchlisted = None
    except ObjectDoesNotExist:
        watchlisted = None
    
    if listing.seller == user:
        seller = True
    elif listing.seller != user:
        seller = False
    
    try:
        bid = listing.bids.get(amount=listing.current_price)
        winner = bid.user
    except ObjectDoesNotExist:
        winner = None

    bids = listing.bids.all()
    number_of_bids = len(bids)

    return render(request, "auctions/listing_page.html", {
        "listing": listing, "bid_form": NewBidForm(),
        "comment_form": NewCommentForm(),
        "comments": comment_objects, "watchlisted": watchlisted, "seller": seller,
        "winner": winner, "number_of_bids": number_of_bids, "message": message, "MEDIA_URL": settings.MEDIA_URL
    })


def handle_bids(request, listing_id):
    form = NewBidForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data["amount"]
        user = User.objects.get(pk=int(request.user.id))
        listing = AuctionListings.objects.get(pk=int(listing_id))
        min_price = int(listing.current_price) + .01
        bids = listing.bids.all()
        if len(bids) == 0:
            min_price = int(listing.current_price)
        if amount < min_price or not listing.active:
            return HttpResponseRedirect(reverse("listing_page_error", args=[(listing_id), ("Invalid Bid.")]))
        
        new_bid = Bid(amount=amount, user=user, listing=listing)
        new_bid.save()

        return HttpResponseRedirect(reverse("listing_page", args=[(listing_id)]))
    else:
        return HttpResponseRedirect(reverse("listing_page_error", args=[(listing_id), ("Invalid Bid.")]))


def handle_comments(request, listing_id):
    form = NewCommentForm(request.POST)
    if form.is_valid():
        comment = form.cleaned_data["comment"]
        user = User.objects.get(pk=int(request.user.id))
        listing = AuctionListings.objects.get(pk=int(listing_id))
        new_comment = Comments(user=user, comment=comment, listing=listing)
        new_comment.save()

        return HttpResponseRedirect(reverse("listing_page", args=[(listing_id)]))
    
    else:
        return HttpResponseRedirect(reverse("listing_page", args=[(listing_id)]))
    

@login_required
def handle_watchlist(request, listing_id):
    if request.method == "POST":
        operation = request.POST["watchlist"]
        user = User.objects.get(pk=int(request.user.id))
        listing = AuctionListings.objects.get(pk=int(listing_id))
        if operation == "Watchlisted":
            watchlist_object = user.watchlisted.get(user=user, listing=listing)
            watchlist_object.delete()

            return HttpResponseRedirect(reverse("listing_page", args=[(listing_id)]))

        elif operation == "Watchlist":
            new_watchlist = WatchListedItem(user=user, listing=listing)
            new_watchlist.save()

            return HttpResponseRedirect(reverse("listing_page", args=[(listing_id)]))
    
    else:
        user = User.objects.get(pk=int(request.user.id))
        watchlisted_listings = user.watchlisted.all()
        watchlisted = [item.listing for item in watchlisted_listings]

        return render(request, "auctions/watchlist.html", {
            "listings": watchlisted, "MEDIA_URL": settings.MEDIA_URL,
        })


def close_auction(request, listing_id):
    listing = AuctionListings.objects.get(pk=listing_id)
    listing.active = False
    listing.save()
    return HttpResponseRedirect(reverse("listing_page", args=[(listing_id)]))


def category_page(request):
    #category_list = sorted(CATEGORIES, key=lambda category: category[1])
    category_list = [category[1] for category in CATEGORIES[1:]]
    category_list = sorted(category_list)
    
    return render(request, "auctions/category_page.html", {
        "categories": category_list,
    })


def category_results(request, category):
    cata_listings = AuctionListings.objects.filter(category=category)
    listings = [listing for listing in cata_listings if listing.active]

    return render(request, "auctions/category_results.html", {
        "listings": listings, "category": category, "MEDIA_URL": settings.MEDIA_URL,
    })