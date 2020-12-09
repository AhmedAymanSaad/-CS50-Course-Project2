from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import User, Listing, WatchList, Comments, Bid

class bidform(forms.Form):
    price = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        self.minprice = kwargs.pop('minprice')
        super(bidform, self).__init__(*args, **kwargs)
        self.fields['price'].widget = forms.NumberInput(attrs={'min':self.minprice})

def index(request):
    listing = Listing.objects.all()
    return render(request, "auctions/index.html",{
        "listing":listing
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


def create_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        image = request.POST["image"]
        category = request.POST["category"]
        user = request.user
        l = Listing(title =title, description = description, image = image, category = category, user=user)
        l.save()
        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/createlisting.html")

def listingpage(request,name):
    entry = Listing.objects.get(title=name)
    user = request.user
    if entry.currprice == None:
        minprice = 1
    else:
        minprice = entry.currprice.price + 1
    if WatchList.objects.filter(user=user,listings=entry):
        watchlist = True
    else:
        watchlist = False

    if request.method == "POST":
        form = bidform(request.POST,minprice=minprice)
        if request.POST.get("addtowatch", False) :
            w = WatchList(user=user,listings=entry)
            w.save()
            return HttpResponseRedirect(reverse("listingpage", args=(name,)))
        elif request.POST.get("removefromwatch", False) :
            w = WatchList.objects.get(user=user,listings=entry)
            w.delete()
            return HttpResponseRedirect(reverse("listingpage", args=(name,)))
        if request.POST.get("closeauction", False) :
            entry.open = False
            entry.save()
            return HttpResponseRedirect(reverse("listingpage", args=(name,)))
        if request.POST.get("commented", False) :
            c = Comments(user=user, content=request.POST["comment"], listing=entry)
            c.save()
        if form.is_valid():
            price = int(form.cleaned_data["price"])
            b = Bid(price=price, user= user)
            b.save()
            if entry.currprice != None:
                entry.currprice.delete()
            entry.currprice = b
            entry.save()
            return HttpResponseRedirect(reverse("listingpage", args=(name,)))
            
    else:
        form = bidform(minprice=minprice)
    return render(request, "auctions/listingpage.html",{
        "name":name,
        "entry":entry,
        "comments":Comments.objects.filter(listing=entry),
        "form":form,
        "watchlist":watchlist
    })

def watchlist(request):
    user = request.user
    wlist = WatchList.objects.filter(user=user)
    return render(request, "auctions/watchlist.html",{
        "wlist":wlist
    })

def categories(request):
    return render(request, "auctions/categories.html",{
        "categorylist":Listing.objects.exclude(category='').values('category').distinct()
    })

def category(request,name):
    return render(request, "auctions/category.html",{
        "name":name,
        "catlist":Listing.objects.filter(category=name)
    })
