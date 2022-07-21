from django.contrib import admin
from .models import User, Listing, Categories

class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "discription")

class CategoriesAdmin(admin.ModelAdmin):
    list_display = ("id", "category")

# Register your models here.
admin.site.register(User)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Categories, CategoriesAdmin)