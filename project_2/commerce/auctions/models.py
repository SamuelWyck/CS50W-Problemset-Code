from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AuctionListings(models.Model):
    name = models.CharField(max_length=64)
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    description = models.CharField(max_length=300)
    starting_price = models.DecimalField(decimal_places=2, max_digits=10)
    @property
    def current_price(self):
        bids = self.bids.all()
        if not bids:
            return self.starting_price
        bids = [bid.amount for bid in bids]
        bids = sorted(bids)
        return bids.pop()
    
    category = models.CharField(max_length=64)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.seller} is selling '{self.name}'."


class Comments(models.Model):
    comment = models.TextField(max_length=400)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    listing = models.ForeignKey(AuctionListings, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"{self.user}'s comment on '{self.listing}'."
    

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    listing = models.ForeignKey(AuctionListings, on_delete=models.CASCADE, related_name="bids")

    def __str__(self):
        return f"{self.user} bid ${self.amount} on {self.listing.name}"
    

class WatchListedItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlisted")
    listing = models.ForeignKey(AuctionListings, on_delete=models.CASCADE)
