from django.contrib.auth import get_user_model
from decimal import Decimal
from .models import Category, Product, Order, Cart
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse
from users.models import Customer, NewUser, Consultant


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



class CategoryViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name="Test category", slug="test-category")

    def test_category_list_view(self):
        response = self.client.get(reverse('category-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'eshop/category_list.html')
        self.assertContains(response, self.category.name)

    def test_product_list_by_category_view(self):
        product = Product.objects.create(name="Test product", unit_price=10, category=self.category, slug="test-product", image = "images/Block_notes_personnalisés.jpg")
        response = self.client.get(reverse('product_list_by_category', kwargs={'category_slug': self.category.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'eshop/product_list_by_category.html')
        self.assertContains(response, self.category.name)
        self.assertContains(response, product.name)

    def test_category_create_view(self):
        consultant = Consultant.objects.create_user(password='testpass', email='consultant@exemple.com', company= "ABC bros")
        self.client.login(username='testuser', password='testpass')
        form_data = {'name': 'New test category', 'slug': 'new-test-category'}
        response = self.client.post(reverse('category-create'), data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('category-list'))
        self.assertTrue(Category.objects.filter(name='New test category', slug='new-test-category').exists())
#
#     def test_category_update_view(self):
#         user = User.objects.create_user(username='testuser', password='testpass')
#         self.client.login(username='testuser', password='testpass')
#         form_data = {'name': 'Updated test category', 'slug': 'updated-test-category'}
#         response = self.client.post(reverse('category-update', kwargs={'slug': self.category.slug}), data=form_data)
#         self.assertEqual(response.status_code, 302)
#         self.assertRedirects(response, reverse('category-list'))
#         self.assertTrue(Category.objects.filter(name='Updated test category', slug='updated-test-category').exists())
#
#     def test_category_delete_view(self):
#         user = User.objects.create_user(username='testuser', password='testpass')
#         self.client.login(username='testuser', password='testpass')
#         response = self.client.post(reverse('category-delete', kwargs={'slug': self.category.slug}))
#         self.assertEqual(response.status_code, 302)
#         self.assertRedirects(response, reverse('category-list'))
#         self.assertFalse(Category.objects.filter(slug=self.category.slug).exists())
#
# class ProductViewsTest(TestCase):
#
#     def setUp(self):
#         self.client = Client()
#         self.category = Category.objects.create(name="Test category", slug="test-category")
#         self.product = Product.objects.create(name="Test product", unit_price=10, category=self.category, slug="test-product")
#
#     def test_products_view(self):
#         response = self.client.get(reverse('products'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'eshop/products.html')
#         self.assertContains(response, self.product.name)
#
#     def test_products_list_mng_view(self):
#         response = self.client.get(reverse('products-list-mng'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'eshop/products_list_mng.html')
