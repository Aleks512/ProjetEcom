from django.urls import path

from . import views

urlpatterns = [
    path('produits/',views.products, name="products"),
    path('produit/<str:slug>/',views.product_detail, name="product"),
    path('produit/<str:slug>/add-to-cart/',views.add_to_cart, name="add-to-cart"),
    path('cart/', views.cart, name='cart')
]
