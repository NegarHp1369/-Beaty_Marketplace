from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import override
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from product.models import Product
from .models import Order, OrderItem, CartItem
from .cart import Cart
from .forms import AddToCartForm
# Create your views here.

class AddToCartView(View):
    form_class = AddToCartForm

    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(product=product, quantity=cd['quantity'], override_quantity=cd['override'])
        return redirect('order:cart_detail')

class CartRemoveView(View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        return redirect('order:cart_detail')


class CartDetailView(View):
    def get(self, request):
        cart = Cart(request)
        for item in cart:
            item['update_quantity_form'] = AddToCartForm(initial={
                'quantity': item['quantity'],
                'override': True
            })
        return render(request, 'order/cart_detail.html', {'cart': cart})

class OrderPaymentView(View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, customer=request.user)
        total = order.total_price
        return render(request, 'order/pay.html', {'order': order, 'total': total})

    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, customer=request.user)
        order.status = 'peid'
        order.save()
        return redirect('order:payment_success', order_id=order.id)

class PaymentSuccessView(View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, customer=request.user)
        return render(request, 'order/payment_success.html',{'order':order})


class CheckoutView(View):
    def post(self, request):
        cart = Cart(request)
        if len(cart) == 0:
            return redirect('order:cart_detail')

        order = Order.objects.create(customer=request.user, status='pending')
        for item in cart:
            OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])

        cart.clear()
        return redirect('order:order_payment', order_id=order.id)


