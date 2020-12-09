from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Bid(models.Model):
    price = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="buyer")

    def __str__ (self):
        return f"{self.price}"

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=64, blank=True)
    image = models.URLField(max_length=64, blank=True)
    category = models.CharField(max_length=64, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller")
    currprice = models.OneToOneField(Bid, on_delete=models.CASCADE, related_name="highestbid", default=Bid, blank=True, null=True)
    open = models.BooleanField(default=True)

    def __str__ (self):
        return f"{self.title}"

class Comments(models.Model):
    content = models.CharField(max_length=1024)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="commenter")

    def __str__ (self):
        return f"{self.user.username}: {self.content}"

class WatchList(models.Model):
    listings = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watchedauction")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
