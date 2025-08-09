from django.urls import path
from .import views
from django.contrib.auth import views as auth_view

app_name = 'accounts'
urlpatterns = [
    path('register/customer/', views.CustomerUserRegister.as_view(), name='customer_register'),
    path('register/seller/', views.SellerRegisterView.as_view(), name='seller_register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('dashboard/seller/', views.SellerDashboardView.as_view(), name='seller_dashboard'),
    path('dashboard/customer/', views.CustomerDashboardView.as_view(), name='customer_dashboard'),

    path('password_reset/', auth_view.PasswordResetView.as_view(template_name='accounts/password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_view.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_view.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),

]