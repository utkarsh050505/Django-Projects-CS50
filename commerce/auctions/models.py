from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):

    category_type = models.CharField(max_length = 64)

    def __str__(self):
        return self.category_type

class Listing(models.Model):

    name = models.CharField(max_length=64)
    description = models.CharField(max_length=400)
    price = models.FloatField()
    image = models.CharField(max_length=1000)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="watch_list")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="winner")

    def __str__(self):
        return self.name


class Bids(models.Model):

    item = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="item")
    highest_bidder = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="bidder")
    highest_bid = models.FloatField(default=0.00)
    number_of_bid = models.IntegerField(default=0)

class Comments(models.Model):

    comment = models.CharField(max_length=150)
    list = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="list")
    user_commenting = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user_commenting")

    def __str__(self):
        return f"{self.user_commenting} comment on {self.list}"
