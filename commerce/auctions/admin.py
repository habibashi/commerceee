from django.contrib import admin
from .models import User, Listing, Categories, Watchlist, Bids, Comment

class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "discription", "categoryID", "bid")

class CategoriesAdmin(admin.ModelAdmin):
    list_display = ("id", "category")

class WatchlistAdmin(admin.ModelAdmin):
    list_display = ("id", "userId", "listId")

class BidsAdmin(admin.ModelAdmin):
    list_display =  ("id", "listId", "userId", "bid")

class commentAdmin(admin.ModelAdmin):
    list_display = ("id", "listId", "userId", "comment")

# Register your models here.
admin.site.register(User)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Watchlist, WatchlistAdmin)
admin.site.register(Bids, BidsAdmin)
admin.site.register(Comment, commentAdmin)