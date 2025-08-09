from django import forms
from .models import CustomerProfile, SellerProfile
from django.contrib.auth.models import User

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = ['phone', 'address']



class SellerProfileForm(forms.ModelForm):
    class Meta:
        model = SellerProfile
        fields = ['phone', 'shop_name', 'address']
