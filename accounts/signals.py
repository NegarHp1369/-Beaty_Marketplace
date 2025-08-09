from django.db.models.signals import post_save
from .models import CustomerProfile, SellerProfile
from django.contrib.auth.models import User
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_staff:
            SellerProfile.objects.create(user=instance)

        else:
            CustomerProfile.objects.create(user=instance)

