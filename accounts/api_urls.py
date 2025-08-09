from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView, TokenBlacklistView
from .views_api import RegisterAPIView,PasswordResetRequestAPIView,PasswordResetConfirmAPIView
urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='api_register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/logout/', TokenBlacklistView.as_view(), name='token_blacklist'),

    path('password_reset/', PasswordResetRequestAPIView.as_view(), name='api_password_reset'),
    path('password_reset/confirm/<uidb64>/<token>/', PasswordResetConfirmAPIView.as_view(), name='api_password_reset_confirm')



]