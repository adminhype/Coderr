from rest_framework.test import APITestCase
from rest_framework import status

from django.contrib.auth.models import User
from django.urls import reverse

from profile_app.models import UserProfile


class LoginTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('login')
        self.username = 'admin'
        self.password = 'strongpassword123'
        self.email = 'admin@example.com'

        self.user = User.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password
        )
        UserProfile.objects.create(
            user=self.user,
            user_type='customer'
        )

    def test_login_success(self):
        data = {
            "username": self.username,
            "password": self.password
        }
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('user_id', response.data)
        self.assertEqual(response.data['username'], self.username)
        self.assertEqual(response.data['email'], self.email)

    def test_login_wrong_password(self):
        data = {
            "username": self.username,
            "password": "wrongpassword"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_missing_fields(self):
        data = {
            "username": self.username,
            # no password
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
