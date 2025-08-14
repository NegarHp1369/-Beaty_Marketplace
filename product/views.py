from unicodedata import category

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product, Category
from .forms import ProductForm
from django.http import HttpResponseForbidden
from django.db.models import Q
from order.forms import AddToCartForm

# Create your views here.

class ProductListView(View):
    def get(self, request):
        products = Product.objects.all()
        cart_form = AddToCartForm()

        search_query = request.GET.get('search', '')
        category = request.GET.get('category')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')


        #search
        if search_query:
            products = products.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))

        #category
        if category:
            products = products.filter(Category__name__iexact=category)

        #min_price
        if min_price:
            products = products.filter(proce__gte=min_price)

        #max_price
        if max_price:
            products = products.filter(price__lte=max_price)

        return render(request, 'product/product_list.html', {'products': products, 'form': cart_form})

class ProductDetailView(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        return render(request, 'product/product_detail.html', {'product': product})


class ProductCreateView(LoginRequiredMixin, View):
    class_form = ProductForm
    template_name = 'product/product_form.html'


    def get(self, request):
        form = self.class_form()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.class_form(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            return redirect('product:product_list')
        return render(request, self.template_name, {'form':form})


class ProductUpdateView(LoginRequiredMixin, View):
    class_form = ProductForm
    template_name = 'product/product_form.html'

    def setup(self, request, *args, **kwargs):
        self.product_instance = get_object_or_404(Product,pk = kwargs['pk'])
        return super().setup(request, *args, **kwargs)


    def get(self, request, *args, **kwargs):
        form = self.class_form(instance=self.product_instance)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.class_form(request.POST, request.FILES, instance=self.product_instance)
        if form.is_valid():
            form.save()
            return redirect('product:product_list')
        return render(request, self.template_name, {'form':form})


class ProductDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk,)
        product.delete()
        return redirect('product:product_list')
