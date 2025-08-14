from django.urls import path
from .import views

app_name = 'order'
urlpatterns = [

    path('cart/', views.CartDetailView.as_view(), name='cart_detail'),
    path('cart/add/<int:product_id>/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.CartRemoveView.as_view(), name='cart_remove'),

    path('order/<int:order_id>/payment/', views.OrderPaymentView.as_view(), name='order_payment'),
    path('order/<int:order_id>/payment/success/', views.PaymentSuccessView.as_view(), name='payment_success'),

    path('checkout/', views.CheckoutView.as_view(), name='checkout')


]