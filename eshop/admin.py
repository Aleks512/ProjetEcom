from django.contrib import admin
from .models import Category, Product, Order, Cart, Comment

# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(Comment)


