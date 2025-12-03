from rest_framework.test import APITestCase
from rest_framework import status

from django.urls import reverse
from profile_app.models import UserProfile
from django.contrib.auth.models import User


class ProfilDetailTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testadmin', email='testadmin@example.com', password='password123')
        self.profile = UserProfile.objects.create(
            user=self.user, user_type='customer', first_name='admin', last_name='works', location='bremen')

        self.client.force_authenticate(user=self.user)

    def test_get_profile_detail(self):
        url = reverse('profile-detail', kwargs={'pk': self.user.pk})
        # url = f'/api/profile/{self.user.pk}/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], self.user.pk)
        self.assertEqual(response.data['first_name'], 'admin')
        self.assertEqual(response.data['email'], 'testadmin@example.com')
        self.assertEqual(response.data['type'], 'customer')
        self.assertEqual(response.data['username'], 'testadmin')
        self.assertEqual(response.data['location'], 'bremen')
