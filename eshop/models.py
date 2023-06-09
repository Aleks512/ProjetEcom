from decimal import Decimal

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from ventalis.settings import AUTH_USER_MODEL


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.slug}/'


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)



class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    description = models.TextField(blank=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, blank=True)

    def __str__(self):
        return self.name

    def price_for_1000_units(self):
        return self.unit_price * Decimal(1000)


    def get_absolute_url(self):
        return reverse("product", kwargs={"slug":self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


QUANTITY_CHOICES = (
    (1000, '1000'),
    (2000, '2000'),
    (3000, '3000'),
    (4000, '4000'),
    (5000, '5000'),
    (6000, '6000'),
    (7000, '7000'),
    (8000, '8000'),
    (9000, '9000'),
    (10000, '10000'),
    # ...
)
class Order(models.Model):
    user = models.ForeignKey('users.Customer', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(choices=QUANTITY_CHOICES, default=1000)
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(blank=True, null=True)
    commentaire = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"

    @property
    def price(self):
        if self.quantity % 1000 != 0:
            raise ValueError("La quantité doit être un multiple de 1000.")
        return self.product.unit_price * (Decimal(self.quantity))



class Cart(models.Model):
    user = models.OneToOneField('users.Customer', on_delete=models.CASCADE)
    orders = models.ManyToManyField(Order)


    def __str__(self):
        return f"Client-{self.user.first_name} {self.user.user_name}"

    def delete(self, *args, **kwargs):
        for order in self.orders.all():
            order.ordered =True
            order.ordered_date = timezone.now()
            order.save()
        self.orders.clear()
        super().delete(*args, **kwargs)

class Comment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='comments')
    consultant = models.ForeignKey('users.Consultant', on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commentaire de {self.consultant.first_name} vontre consultant Ventalis pour la commande {self.order.product.name} ({self.order.quantity})"
