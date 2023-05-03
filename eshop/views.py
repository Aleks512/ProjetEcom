from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from eshop.models import Product, Cart, Order

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
        return redirect(reverse('products'))

    customer = user.customer
    product = get_object_or_404(Product, slug=slug)
    cart, _ = Cart.objects.get_or_create(user=customer)
    order, created = Order.objects.get_or_create(user=customer, ordered=False, product=product)

    if created:
        cart.orders.add(order)
        cart.save()
    else:
        order.quantity += 1000
        order.save()

    # price = product.price_for_quantity(order.quantity)
    # order.price = price
    # order.save()

    messages.success(request, f"{product.name} a été ajouté à votre panier.")
    return redirect(reverse("product", kwargs={'slug': slug}))


def cart(request):
    cart = get_object_or_404(Cart, user=request.user.customer)
    orders = cart.orders.all()
    total_price = 0
    for order in orders:
        total_price += order.price
    return render(request, "eshop/cart.html", context={"orders":orders, "total_price":total_price})



def cart_delete(request):
    if cart:=request.user.customer.cart:
        cart.orders.all().delete()
        cart.delete()
    return redirect("home")



