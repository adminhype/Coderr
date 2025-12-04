from rest_framework.test import APITestCase
from rest_framework import status

from django.contrib.auth.models import User
from django.urls import reverse

from profile_app.models import UserProfile


class ProfileListTests(APITestCase):
    def setUp(self):
        self.bob_user = User.objects.create_user(
            username='bob', email='bob@example.com', password='password123')
        UserProfile.objects.create(
            user=self.bob_user, user_type='business', first_name='bob')

        self.bobby_user = User.objects.create_user(
            username='bobby', email='bobby@example.com', password='password123')
        UserProfile.objects.create(
            user=self.bobby_user, user_type='business', first_name='bobby')

        self.ado_user = User.objects.create_user(
            username='ado', email='ado@example.com', password='password123')
        UserProfile.objects.create(
            user=self.ado_user, user_type='customer', first_name='ado')

        self.client.force_authenticate(user=self.bob_user)

    def test_list_business_profiles(self):
        url = 'api/profiles/business/'

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        for profile in response.data:
            self.assertEqual(profile['type'], 'business')

    def test_list_customer_profiles(self):
        url = 'api/profiles/customer/'

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['type'], 'customer')
        self.assertEqual(response.data[0]['first_name'], 'ado')
