from django.urls import path

from . import views

urlpatterns = [
    path('produits/',views.products, name="products"),
    path('products/list/manage/', views.products_list_mng, name='products-list-mng'),
    path('produit/<str:slug>/',views.product_detail, name="product"),
    path('produit/<str:slug>/add-to-cart/',views.add_to_cart, name="add-to-cart"),
    path('cart/', views.cart, name='cart'),
    path('cart/delete/', views.cart_delete, name='cart-delete'),
    path('category/list/', views.category_list, name='category-list'), #ok
    path('category/create/', views.category_create_view, name='category-create'),

    path('category/<slug:category_slug>/', views.product_list_by_category, name='product_list_by_category'),
    #path('categories/<slug:category_slug>/', views.product_list_by_category, name='product-list-by-category'),

    path('category/<slug:slug>/update/', views.category_update_view, name='category-update'),
    path('category/<slug:slug>/delete/', views.category_delete_view, name='category-delete'),
    #path('products/<slug:category_slug>/', views.product_list, name='product-list'),
    path('product/create/', views.product_create_view, name='product-create'),
    path('product/<slug:slug>/update/', views.product_update_view, name='product-update'),
    path('product/<slug:slug>/delete/', views.product_delete_view, name='product-delete'),


    # Path pour la mise à jour de la commande
    path('orders/<int:pk>/update/', views.OrderUpdateConsultantView.as_view(), name='consultant-order-update'),#OK
    path('order/<pk>/update', views.OrderCustomerUpdateView.as_view(), name='order-update'),#ok
    # Path pour la visualisation des détails de la commande
    path('orders/<int:order_id>/', views.OrderDetailView.as_view(), name='order_detail'),


    #path('consultant/order/<pk>/update', views.OrderConsultantUpdateView.as_view(), name='order-consultant-update'),
    path('order/<pk>/delete', views.OrderDeleteView.as_view(), name='order-delete'),# a checker

    path('cart-delete/', views.cart_delete, name='cart_delete'),
    path('checkout/', views.checkout, name='checkout'),

    path('order/detail/<pk>', views.OrderDetailView.as_view(), name='order-detail'),# OK


    path('categories/', views.category_list, name='category-list'),


]
