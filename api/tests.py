from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

from users.models import Customer, Consultant


class CustomerSendMessageAPIViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Créer un customer pour tester
        #self.consultant = self.customer.consultant_applied
        self.consultant = Consultant.objects.create(
             user_name = "const1",
             email='consultant@example.com',
             password='password',
             # Autres champs du modèle Consultant
        )

        self.customer = Customer.objects.create(
            user_name = "cust1",
            email='customer@example.com',
            password='password',
            # Autres champs du modèle Customer
            consultant_applied = self.consultant
        )

        self.client.force_authenticate(user=self.customer)

    def test_create_message_unauthenticated(self):
        self.client.logout()
        url = '/api/customer/messages/send/'
        data = {
            'content': 'Test message',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_message(self):
        url = '/api/customer/messages/send/'
        data = {
            'content': 'Test message',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Vérifier si le message a été créé avec les bonnes valeurs
        self.assertEqual(response.data['sender'], self.customer.id)
        self.assertEqual(response.data['recipient'], self.consultant.id)
        self.assertEqual(response.data['content'], 'Test message')

