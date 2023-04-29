from decimal import Decimal

from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    description = models.TextField(blank=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def price_for_quantity(self, quantity):
        if quantity % 1000 != 0:
            raise ValueError("La quantité doit être un multiple de 1000.")
        return self.unit_price * (Decimal(quantity) / Decimal('1000'))
