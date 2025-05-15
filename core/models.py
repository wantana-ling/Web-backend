# core/models.py
from django.db import models
from django.utils import timezone

class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    rank = models.IntegerField(default=1)

    def __str__(self):
        return self.username

class CoreDetail(models.Model):
    product_name = models.CharField(max_length=100)
    product_description = models.TextField()
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_rank = models.IntegerField(default=1)
    product_color = models.CharField(max_length=100,default="bg-blue-600")

    def __str__(self):
        return self.product_name
    
class Donation(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='donations')
    product = models.ForeignKey('CoreDetail', on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(default=timezone.now)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount} THB"
    

