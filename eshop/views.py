from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from eshop.models import Product, Cart, Order
from users.models import Customer
from django.contrib.messages import get_messages

# Create your views here.

def products(request):
    products = Product.objects.all()

    return render(request, "eshop/products.html", context={"products":products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, "eshop/product_detail.html", context={"product":product})



def add_to_cart(request, slug):
    user = request.user

    if not user.is_authenticated:
        messages.info(request, "Vous devez être connecté pour ajouter des produits au panier.")
        return redirect(reverse('login'))

    if user.is_superuser or user.is_employee:
        messages.warning(request, "Vous n'êtes pas autorisé à ajouter des produits au panier.")
        return redirect(reverse('home'))

    if not user.is_client:
        messages.info(request, "Vous êtes identifié, mais vous n'êtes pas un client. Vous pouvez continuer à naviguer.")
        return redirect(reverse('product', kwargs={'slug': slug}))

    customer = user.customer
    product = get_object_or_404(Product, slug=slug)
    cart, _ = Cart.objects.get_or_create(user=customer)
    order, created = Order.objects.get_or_create(user=customer, product=product)

    if created:
        cart.orders.add(order)
        cart.save()
    else:
        order.quantity += 1000
        order.save()

    messages.success(request, f"{product.name} a été ajouté à votre panier.")
    return redirect(reverse("product", kwargs={'slug': slug}))


def cart(request):
    cart = get_object_or_404(Cart,user = request.user.customer)

    return render(request, "eshop/cart.html", context={"orders":cart.orders.all()})



