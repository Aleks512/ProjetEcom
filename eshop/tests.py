from django.test import TestCase
from decimal import Decimal
from .models import Category, Product


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

    def test_price_for_quantity(self):
        # Test with quantity in hundreds
        with self.assertRaises(ValueError):
            price = self.test_product.price_for_quantity(500)

        # Test with quantity not in thousands
        with self.assertRaises(ValueError):
            price = self.test_product.price_for_quantity(1500)

        # Test with quantity in thousands
        price = self.test_product.price_for_quantity(2000)
        self.assertEqual(price, Decimal('20.00'))

        # Test with quantity in thousands and decimal places
        with self.assertRaises(ValueError):
            price = self.test_product.price_for_quantity(2.5)

    def test_price_for_quantity2(self):
        category = Category.objects.create(name="category name")
        product = Product.objects.create(name='Produit de test', unit_price=Decimal('1.00'), stock=10, category=category)
        with self.assertRaises(ValueError):
            product.price_for_quantity(500)
        self.assertEqual(product.price_for_quantity(1000), Decimal('1.00'))
        self.assertEqual(product.price_for_quantity(2000), Decimal('2.00'))


class CategoryModelTests(TestCase):
    def test_cat_slug(self):
        # Créer une nouvelle catégorie avec un nom et un slug vides
        category = Category.objects.create(name="Test Category")

        # Vérifier que le slug a été généré automatiquement avec le nom de la catégorie
        self.assertEqual(category.slug, "test-category")