from django.db import models
from django.contrib.auth.models import User

class CustomerProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cuser')
    phone = models.CharField(max_length=11)
    address = models.TextField(max_length=200)

    def __str__(self):
        return self.user.username


class SellerProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='suser')
    phone = models.CharField(max_length=11)
    shop_name = models.CharField(max_length=100)
    address = models.TextField(max_length=200)

    def __str__(self):
        return self.shop_name



