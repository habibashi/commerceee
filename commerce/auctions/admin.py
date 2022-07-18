from django.contrib import admin
from .models import User, CreateList, Categories

# class CreateListAdmin(admin.ModelAdmin):
#     list_display = ("id", "title", "description")

class CategoriesAdmin(admin.ModelAdmin):
    list_display = ("id", "category")

# Register your models here.
admin.site.register(User)
admin.site.register(CreateList)
admin.site.register(Categories, CategoriesAdmin)