from django.shortcuts import render

from eshop.models import Product


# Create your views here.

def products(request):
    products = Product.objects.all()

    return render(request, "eshop/products.html", context={"products":products})

def product_detail(request):
    pass