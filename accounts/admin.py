from django.contrib import admin
from .models import CustomerProfile, SellerProfile

admin.site.register(SellerProfile)
admin.site.register(CustomerProfile)
