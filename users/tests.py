from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import CustomAccountManager, NewUser, Consultant, Customer


class UserAccountTests(TestCase):

    def test_new_superuser(self):
        db = get_user_model()
        super_user = db.objects.create_superuser(
            'testuser@super.com', 'password')
        self.assertEqual(super_user.email, 'testuser@super.com')
        self.assertTrue(super_user.is_superuser)
        self.assertTrue(super_user.is_staff)
        self.assertTrue(super_user.is_active)
        self.assertEqual(str(super_user), "Administrateur")

        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                email='testuser@super.com', password='password', is_superuser=False)

        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                email='testuser@super.com',password='password', is_staff=False)

        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                email='', password='password', is_superuser=True)


class CustomAccountManagerTestCase(TestCase):
    def test_create_user(self):
        User = get_user_model()
        email = 'test@example.com'
        password = 'testpassword'
        company = 'Test Company'

        # Create a new user
        user = User.objects.create_user(
            email=email,
            password=password,
            company=company,
        )

        # Check that the user was created
        self.assertIsNotNone(user)

        # Check that the user's email and company are correct
        self.assertEqual(user.email, email)
        self.assertEqual(user.company, company)

        # Check that the user's password was set correctly
        self.assertTrue(user.check_password(password))

