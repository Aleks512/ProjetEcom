
from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import  Consultant


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



