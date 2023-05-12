
from django.test import TestCase
from django.urls import reverse
from contact.forms import ContactForm
from contact.views import ContactView, ContactSuccessView

class ContactViewTestCase(TestCase):
    def test_contact_form_submission(self):
        # Test that the form submission is successful
        form_data = {
            'nom': 'John Doe',
            'email': 'johndoe@example.com',
            'sujet': 'Test subject',
            'message': 'This is a test message'
        }
        response = self.client.post(reverse('contact:contact'), data=form_data)
        self.assertEqual(response.status_code, 302)  # 302 is the redirect status code
        self.assertRedirects(response, reverse('contact:success'))

        # Test that the form sends an email
        # (Assuming that the form send method is implemented properly)
        # To check if the email was sent, you can use a mail testing library like Mailhog, Mailtrap, etc.
        # or check if the send() method was called using a mock object.

class ContactSuccessViewTestCase(TestCase):
    def test_success_page(self):
        response = self.client.get(reverse('contact:success'))
        self.assertEqual(response.status_code, 200)  # 200 is the success status code
        self.assertTemplateUsed(response, 'contact/success.html')
