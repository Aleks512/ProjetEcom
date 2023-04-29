from django.urls import path

from . import views

urlpatterns = [

    path('',views.products, name="products"),
    path('produit/<str:slug>/',views.product_detail, name="product"),
]
