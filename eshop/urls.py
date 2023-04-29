from django.urls import path

from . import views

urlpatterns = [

    path('produits/',views.products, name="products"),
]
