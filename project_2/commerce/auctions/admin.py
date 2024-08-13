from django.contrib import admin
from .models import AuctionListings, Bid, Comments, User, WatchListedItem


class AuctionListingsAdmin(admin.ModelAdmin):
    list_display = ("id", "seller", "name", "current_price", "image", "category", "description", "active")


class WatchlistedItemAdmin(admin.ModelAdmin):
    list_display = ("user", "listing")


# Register your models here.
admin.site.register(AuctionListings, AuctionListingsAdmin)
admin.site.register(Bid)
admin.site.register(Comments)
admin.site.register(User)
admin.site.register(WatchListedItem, WatchlistedItemAdmin)