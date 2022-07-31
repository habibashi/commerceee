from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass

class Categories(models.Model):
    category = models.CharField(max_length=70)

    def __str__(self):
        return f"{self.category}"


class Listing(models.Model):
    title = models.CharField(max_length=64)
    discription = models.CharField(max_length=64)
    bid = models.FloatField(max_length=100)
    urlImage = models.ImageField(max_length=700)
    categoryID = models.ForeignKey(Categories, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    startTime = models.DateTimeField(auto_now=False, auto_now_add=False)
    endTime = models.DateTimeField(auto_now=False, auto_now_add=False)
    userId = models.ForeignKey(User, on_delete=models.CASCADE, related_name="buyer", null=True)
    close = models.BooleanField(default=False)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.title} {self.discription} {self.bid}"

class Watchlist(models.Model):
    title = models.CharField(max_length=64)
    discription = models.CharField(max_length=64)
    bid = models.FloatField(max_length=50)
    urlImage = models.ImageField(max_length=700)
    categoryID = models.ForeignKey(Categories, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    startTime = models.DateTimeField(auto_now=False, auto_now_add=False)
    endTime = models.DateTimeField(auto_now=False, auto_now_add=False)
    userId = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    listId = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.title} {self.discription}"

class Bids(models.Model):
    bid = models.FloatField(max_length=50)
    listId = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True)
    userId = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.bid}"

class Comment(models.Model):
    comment = models.CharField(max_length=100)
    listId = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True)
    userId = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.comment}"