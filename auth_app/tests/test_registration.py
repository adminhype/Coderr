from rest_framework.test import APITestCase
from rest_framework import status

from django.contrib.auth.models import User
from django.urls import reverse


class RegistrationTestCase(APITestCase):

    def setUp(self):
        # self.url = '/api/registration/'
        self.url = reverse('registration')

    def test_registration_success(self):
        data = {
            'username': 'adminhype',
            'email': 'adminhype@example.com',
            'password': 'strongpassword123',
            'repeated_password': 'strongpassword123',
            'type': 'customer'
        }
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertIn('token', response.data)
        self.assertIn('user_id', response.data)
        self.assertEqual(response.data['username'], data['username'])
        self.assertEqual(response.data['email'], data['email'])

    def test_registation_password_mismatch(self):
        data = {
            'username': 'adminhype',
            'email': 'adminhype@example.com',
            'password': 'strongpassword123',
            'repeated_password': 'wrongpassword',
            'type': 'customer'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_email_already_exists(self):
        User.objects.create_user(
            username='existinguser', email='adminhype@example.com', password='somepassword')
        data = {
            'username': 'second',
            'email': 'adminhype@example.com',
            'password': 'strongpassword123',
            'repeated_password': 'strongpassword123',
            'type': 'customer'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
