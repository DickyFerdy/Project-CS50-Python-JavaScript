from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime


class User(AbstractUser):
    pass


class Category(models.Model):
    categoryName = models.CharField(max_length=100)
    
    def __str__(self):
        return self.categoryName
    
    
class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid_user")
    bid = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.bid}"


class Listing(models.Model):
    title = models.CharField(max_length=100, blank=False)
    description = models.CharField(max_length=300, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    bidPrice = models.ForeignKey(Bid, on_delete=models.SET_NULL, blank=True, null=True, related_name="bid_price")
    imageURL = models.CharField(max_length=500, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=False, null=True, related_name="category")
    isActive = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing_owner")
    postTime = models.DateTimeField(default=datetime.datetime.now)
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="listing_watchlist")

    def __str__(self):
        return self.title

    def format_posting(self):
        return self.postTime.strftime("Created %d %b %Y, %I:%M %p")
    
    
class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE , related_name="user_transaction")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_transaction")
    bid = models.ForeignKey(Bid, on_delete=models.CASCADE, related_name="bid_transaction")

    def __str__(self):
        return f"{self.listing} by {self.user} at {self.bid}"
    
    
class Comments(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author_comment")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_comment")
    message = models.CharField(max_length=300)
    postTime = models.DateTimeField(default=datetime.datetime.now)
    
    def __str__(self):
        return f"{self.author} comment on {self.listing}"
        
    def format_posting(self):
        return self.postTime.strftime("%d %b %Y, %I:%M %p")