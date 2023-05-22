from django.contrib.auth import get_user_model
from decimal import Decimal
from .models import Category, Product, Order
from django.test import TestCase, Client
from django.urls import reverse
from users.models import Customer, NewUser


User = get_user_model()

class EshopModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a test category
        cls.test_category = Category.objects.create(name='Test Category')

        # Create a test product
        cls.test_product = Product.objects.create(
            name='Test Product',
            unit_price=Decimal('10.00'),
            stock=100,
            category=cls.test_category,
        )

    def test_category_str(self):
        self.assertEqual(str(self.test_category), 'Test Category')

    def test_product_str(self):
        self.assertEqual(str(self.test_product), 'Test Product')

# Calcul de prix
class OrderModelTests(TestCase):
    def setUp(self):
        # Créer une catégorie pour le produit
        self.category = Category.objects.create(name='Category1')
        # Créer un produit pour tester
        self.product = Product.objects.create(name='Product1', unit_price=Decimal('10.00'),
                                              category=self.category)
        # Créer un customer pour tester
        self.customer = Customer.objects.create(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",)
    # Calcule de prix avec une quantité en milliers
    def test_price_with_valid_quantity(self):
        order = Order.objects.create(user=self.customer, product=self.product, quantity=2000)
        self.assertEqual(order.price, Decimal('20000.00'))

    # Calcule de prix avec une quantité en milliers
    def test_price_with_invalid_quantity(self):
        order = Order.objects.create(user=self.customer,product=self.product, quantity=1500)
        with self.assertRaises(ValueError):
            order.price



class CategoryModelTests(TestCase):
    def test_cat_slug(self):
        # Créer une nouvelle catégorie avec un nom et un slug vides
        category = Category.objects.create(name="Test Category")

        # Vérifier que le slug a été généré automatiquement avec le nom de la catégorie
        self.assertEqual(category.slug, "test-category")




class CategoryCreateViewTest(TestCase):
    def setUp(self):
        # Créer un utilisateur de test avec l'attribut is_employee=True
        self.employee_user = NewUser.objects.create(
            email='employee@example.com',
            password='password123',
            is_employee=True
        )

        # Créer un client pour effectuer les requêtes HTTP
        self.client = Client()

        # Connecter l'utilisateur de test
        self.client.force_login(self.employee_user)

        # Définir les URLs pour les vues de création et de liste des catégories
        self.create_category_url = reverse('category-create')
        self.category_list_url = reverse('category-list')





