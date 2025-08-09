from pyexpat.errors import messages

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from jwt.utils import force_bytes
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import CustomerProfile, SellerProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

        def create(self, validated_data):
            user = User(username=validated_data['username'], email=validated_data['email'])

            user.set_password(validated_data['password'])
            user.save()
            return user


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError('doesnt exist any user by this email.')
        return value

    def save(self):
        email = self.validated_data['email']
        user = User.objects.filter(email=email).first()
        if user:
            uid = urlsafe_base64_encode((force_bytes(user.pk)))
            token = default_token_generator.make_token(user)
            reset_url = f'https://127.0.0.1:8000/api/accounts/password_reset/confirm/{uid}/{token}/'
            subject = 'retrieve password'
            messages = render_to_string('accounts/password_reset_email.txt', {
                   'user': user,
                   'reset_url': reset_url
            })
            send_mail(subject, messages, settings.DEFAULT_FROM_EMAIL, [user.email])
