
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import OrderItem, Order
from product.models import Product
from .cart import Cart
from .serializer import OrderSerializer, OrderItemSerializer, ProductSerializer

class CartViewSet(viewsets.ViewSet):
    def list(self, request):
        cart = Cart(request)
        data = []
        for item in cart:
            data.append({
                'product': ProductSerializer(item['product']).data,
                'quantity': item['quantity'],
                'price': float(item['price']),
                'total_price': float(item['price']*item['quantity'])

            })
        return Response(data)

    @action(detail=False, methods=['post'], url_path='add')
    def add_to_cart(self, request):
        cart = Cart(request)
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))
        override = request.data.get('override', False)
        product = Product.objects.get(id=product_id)
        cart.add(product=product, quantity=quantity, override_quantity=override)
        return Response({'message': 'Product added to cart'})

    @action(detail=False, methods=['post'], url_path='remove')
    def remove_from_cart(self, request):
        cart = Cart(request)
        product_id = request.data.get('product_id')
        product = Product.objects.get(id=product_id)
        cart.remove(product)
        return Response({'message': 'Product remove from cart'})


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def create(self, request, *args, **kwargs):
        cart = Cart(request)
        if len(cart) == 0:
            return Response({'error':'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(customer=request.user, status='pending')
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity']
            )

        cart.clear()
        serializer = self.get_serializer(order)
        return Response(serializer.data)
