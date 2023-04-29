from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from eshop.models import Product


# Create your views here.

def products(request):
    products = Product.objects.all()

    return render(request, "eshop/products.html", context={"products":products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, "eshop/product_detail.html", context={"product":product})