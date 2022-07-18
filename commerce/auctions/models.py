from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass

class Categories(models.Model):
    category = models.CharField(max_length=70)

    def __str__(self):
        return f"{self.category}"


class CreateList(models.Model):
    title = models.CharField(max_length=64)
    discription = models.CharField(max_length=64)
    bid = models.FloatField(max_length=50)
    urlImage = models.ImageField(max_length=700)
    categoryID = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name="categoryiess", null=True)
    created_at = models.DateTimeField(default=timezone.now)
    startTime = models.DateTimeField(auto_now=False, auto_now_add=False)
    endTime = models.DateTimeField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return f"{self.title} {self.discription}"