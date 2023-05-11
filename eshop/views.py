from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from django.utils import timezone
from django.views.generic import UpdateView, DeleteView

from eshop.models import Product, Cart, Order, Category
from .forms import CategoryCreateForm, CategoryUpdateForm, CategoryDeleteForm, ProductCreateForm, ProductUpdateForm, \
    ProductDeleteForm


class OrderUpdateView(UpdateView):
  model= Order
  template_name= "eshop/order_update.html"
  fields = ('product', 'quantity',)

  def get_success_url(self):
      return '/cart'
class OrderDeleteView(DeleteView):
    model = Order
    template_name = "eshop/order_delete.html"
    fields = '__all__'
    def get_success_url(self):
        return '/cart'


def category_list(request):
    categories = Category.objects.all()
    context = {"categories": categories}
    return render(request, 'eshop/category_list.html', context)

def product_list_by_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    context = {'category': category, 'products': products}
    return render(request, 'eshop/product_list_by_category.html', context)

@login_required
def category_create_view(request):
    if not request.user.is_authenticated or not request.user.is_employee:
        return HttpResponseForbidden("Vous n'êtes pas autorisé à accéder à cette page.")
    form = CategoryCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('category-list')
    return render(request, 'eshop/category_create.html', {'form': form})

@login_required()
def category_update_view(request, slug):
    if not request.user.is_authenticated or not request.user.is_employee:
        return HttpResponseForbidden("Vous n'êtes pas autorisé à accéder à cette page.")
    category = get_object_or_404(Category, slug=slug)
    form = CategoryUpdateForm(request.POST or None, instance=category)
    if form.is_valid():
        form.save()
        return redirect('category-list')
    return render(request, 'eshop/category_update.html', {'form': form, 'category': category})

@login_required()
def category_delete_view(request, slug):
    if not request.user.is_authenticated or not request.user.is_employee:
        return HttpResponseForbidden("Vous n'êtes pas autorisé à accéder à cette page.")
    category = get_object_or_404(Category, slug=slug)
    form = CategoryDeleteForm(request.POST or None, instance=category)
    if request.method == 'POST':
        category.delete()
        messages.success(request, f'La catégorie "{category.name}" a été supprimée avec succès.')
        return redirect(reverse('category-list'))
    return render(request, 'eshop/category_delete.html', {'form': form, 'category': category})
def products(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, "eshop/products.html", context={"products": products, "categories": categories})


@login_required()
def products_list_mng(request):
    if not request.user.is_authenticated or not request.user.is_employee:
        return HttpResponseForbidden("Vous n'êtes pas autorisé à accéder à cette page.")
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, "eshop/products_list_mng.html", context={"products":products, "categories": categories})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, "eshop/product_detail.html", context={"product":product})

@login_required()
def product_create_view(request):
    if not request.user.is_authenticated or not request.user.is_employee:
        return HttpResponseForbidden("Vous n'êtes pas autorisé à accéder à cette page.")
    form = ProductCreateForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('products-list-mng')
    return render(request, 'eshop/product_create.html', {'form': form})

@login_required()
def product_update_view(request, slug):
    if not request.user.is_authenticated or not request.user.is_employee:
        return HttpResponseForbidden("Vous n'êtes pas autorisé à accéder à cette page.")
    product = get_object_or_404(Product, slug=slug)
    form = ProductUpdateForm(request.POST or None, request.FILES or None, instance=product)
    if form.is_valid():
        form.save()
        return redirect('products-list-mng')
    return render(request, 'eshop/product_update.html', {'form': form, 'product': product})

@login_required()
def product_delete_view(request, slug):
    if not request.user.is_authenticated or not request.user.is_employee:
        return HttpResponseForbidden("Vous n'êtes pas autorisé à accéder à cette page.")
    product = get_object_or_404(Product, slug=slug)
    form = ProductDeleteForm(request.POST or None, instance=product)
    if request.method == 'POST':
        product.delete()
        return redirect('products-list-mng')
    return render(request, 'eshop/product_delete.html', {'form': form, 'product': product})
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

    messages.success(request, f"{product.name} a été ajouté à votre panier.")
    return redirect(reverse("product", kwargs={'slug': slug}))


def cart(request):
    cart = get_object_or_404(Cart, user=request.user.customer)
    orders = cart.orders.all()
    total_price = 0
    for order in orders:
        total_price += order.price
    return render(request, "eshop/cart.html", context={"orders":orders, "total_price":total_price})


@login_required
def cart_delete(request):
    if cart:=request.user.customer.cart:
        cart.orders.all().delete()
        cart.delete()
    return redirect("products")

@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    for order in cart.orders.all():
        order.ordered = True
        order.ordered_date = timezone.now()
        order.save()
    cart.orders.clear()
    messages.success(request, 'Votre commande a été passée avec succès. Merci!')
    return redirect(reverse('products'))


