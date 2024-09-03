from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from .models import User

# Create your tests here.


class RegistrationCreateViewTestCase(TestCase):

    def setUp(self):
        self.path = reverse('users:registration')
        self.data = {
            'first_name': 'Atageldi',
            'last_name': 'Durdyev',
            'password1': 'Atashka2003',
            'password2': 'Atashka2003',
            'email': 'durdyyevatageldi03@gmail.com',
            'username': 'Ata'
        }

    def test_registration_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store - Registration')
        self.assertTemplateUsed(response, 'users/registration.html')

    def test_registration_post(self):
        response = self.client.post(self.path, self.data)
        username = self.data['username']

        # Check user
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:login'))
        self.assertTrue(User.objects.filter(username=username).exists())

    def test_registration_post_error(self):
        User.objects.create(username=self.data['username'])
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, '')

