from rest_framework.response import Response
from rest_framework import viewsets, permissions
from .serializers import ProductSerializers
from .models import Product, Category
from rest_framework.decorators import action
from rest_framework import filters
from django.db.models import Q



class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('-id')
    serializer_class = ProductSerializers
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

    def get_queryset(self):
        queryset = Product.objects.all()

        category = self.request.query_params.get('category')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')

        if category:
            queryset = queryset.filter(category__name__icontains=category)

        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        return queryset

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

    def perform_update(self, serializer):
        if self.request.user != serializer.instance.seller:
            raise permissions.PermissionDenied('you are not allow to edit this product')
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user != instance.seller:
            raise permissions.PermissionDenied("you are not allow to delete this product")
        instance.delete()

    @action(detail=False, methods=["get"], permission_classes=[permissions.IsAuthenticated])

    def my_products(self, request):
        products = self.queryset.filter(seller=request.user)
        serializer = self.serializer_class(products, many=True)
        return Response(serializer.data)
