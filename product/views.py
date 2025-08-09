from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product
from .forms import ProductForm

# Create your views here.

class ProductListView(View):
    def get(self, request):
        products = Product.objects.all()
        return render(request, 'product/product_list.html', {'product': products})

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

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk, seller=request.user)
        form = self.class_form(instance=product)
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk, seller=request.user)
        form = self.class_form(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product:product_list')
        return render(request, self.template_name, {'form':form})


class ProductDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk, seller=request.user)
        product.delete()
        return redirect('product:product_list')
