from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from .models import Consultant, Customer, NewUser
from django.urls import reverse
from django.contrib.auth.models import Permission


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




class ConsultantModelTest(TestCase):
    def setUp(self):
        self.consultant = Consultant.objects.create(
            user_name='testuser',
            email='test@example.com',
            first_name='Test',
            last_name='User',
            company='Test Company'
        )

    def test_generate_random_matricule(self):
        matricule = self.consultant.generate_random_matricule()
        self.assertEqual(len(matricule), Consultant.MATRICULE_LENGTH)

    def test_save_with_unique_matricule(self):
        consultant2 = Consultant.objects.create(
            user_name='testuser2',
            email='test2@example.com',
            first_name='Test',
            last_name='User',
            company='Test Company'
        )
        self.assertNotEqual(self.consultant.matricule, consultant2.matricule)

    class ConsultantTestCase(TestCase):
        def setUp(self):
            self.user1 = User.objects.create(
                username='user1',
                email='user1@example.com',
                password='password1',
                customer=False,
                company='Ventalis'
            )

            self.user2 = User.objects.create(
                username='user2',
                email='user2@example.com',
                password='password2',
                customer=False,
                company='Ventalis'
            )

            self.consultant1 = Consultant.objects.create(
                user=self.user1,
                clients_number=0
            )

            self.consultant2 = Consultant.objects.create(
                user=self.user2,
                clients_number=2
            )

        def test_assign_consultant_to_client(self):
            user3 = User.objects.create(
                username='user3',
                email='user3@example.com',
                password='password3',
                customer=True,
                company='ABC Corp'
            )
            consultant = Consultant.assign_consultant_to_client(user3)
            customer = Customer.objects.filter(consultant_applied=user3).first()

            self.assertEqual(customer.company, user3.company)
            self.assertEqual(customer.consultant, consultant)
            self.assertEqual(consultant.clients_number, 1)

        def test_assign_consultant_to_client_with_existing_consultant(self):
            user4 = User.objects.create(
                username='user4',
                email='user4@example.com',
                password='password4',
                customer=True,
                company='XYZ Inc'
            )
            consultant = Consultant.assign_consultant_to_client(user4)
            customer = Customer.objects.filter(consultant_applied=user4).first()

            self.assertEqual(customer.company, user4.company)
            self.assertEqual(customer.consultant, self.consultant2)
            self.assertEqual(consultant, None)

        def test_assign_consultant_to_client_with_no_consultants(self):
            user5 = User.objects.create(
                username='user5',
                email='user5@example.com',
                password='password5',
                customer=True,
                company='DEF LLC'
            )
            consultant = Consultant.assign_consultant_to_client(user5)

            self.assertEqual(consultant, None)

class CustomerListViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.user = get_user_model().objects.create_superuser(
            email='testuser1@example.com',
            password='testpass'
        )
        cls.customer1 = Customer.objects.create(
            consultant_applied=None,
        )

    def test_customer_list_view(self):
        self.client.login(email=self.user.email, password='testpass')
        response = self.client.get(reverse('customers-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/customers_list.html')
        self.assertContains(response, 'Liste de clients')




class ConsultantListViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.user = get_user_model().objects.create_superuser(
            email='testuser@example.com',
            password='testpass'
        )
        cls.permission = Permission.objects.get(name='Can view consultant')
        cls.consultant = Consultant.objects.create(
            matricule='ABCD',
            email='consultant1@example.com'
        )
        cls.consultant.user_permissions.add(cls.permission)

    def test_consultant_list_view(self):
        self.client.login(email=self.user.email, password='testpass')
        response = self.client.get(reverse('consultant-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/consultant_list.html')
        self.assertContains(response, self.consultant.matricule)
        self.assertContains(response, self.consultant.email)
        self.assertContains(response, self.consultant.get_clients_count())
