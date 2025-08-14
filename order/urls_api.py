from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views_api import CartViewSet, OrderViewSet

router = DefaultRouter()
router.register('cart', CartViewSet, basename='cart')
router.register('order', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
