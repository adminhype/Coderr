from rest_framework.test import APITestCase
from rest_framework import status

from django.contrib.auth.models import User
from django.urls import reverse

from profile_app.models import UserProfile


class ProfileUpdateTest(APITestCase):
    def setUp(self):
        self.owner_user = User.objects.create_user(
            username='owner', email='owner@example.com', password='password123')
        self.owner_profile = UserProfile.objects.create(
            user=self.owner_user, user_type='business', first_name='Owner', location='bremen')

        self.attacker_user = User.objects.create_user(
            username='attacker', email='attacker@example.com', password='password123')
        self.attacker_profile = UserProfile.objects.create(
            user=self.attacker_user, user_type='customer')

        self.url = reverse('profile-detail', kwargs={'pk': self.owner_user.pk})

    def test_update_own_profile_success(self):
        self.client.force_authenticate(user=self.owner_user)

        data = {
            'first_name': 'newowner',
            'email': 'newowner@example.com',
            'location': 'hamburg'
        }

        response = self.client.patch(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['first_name'], 'newowner')
        self.assertEqual(response.data['email'], 'newowner@example.com')

        self.owner_profile.refresh_from_db()
        self.assertEqual(self.owner_profile.first_name, 'newowner')

        self.owner_profile.user.refresh_from_db()
        self.assertEqual(self.owner_profile.user.email, 'newowner@example.com')

    def test_update_other_profile_forbidden(self):
        self.client.force_authenticate(user=self.attacker_user)

        data = {
            'first_name': 'hacked'
        }

        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.owner_profile.refresh_from_db()
        self.assertNotEqual(self.owner_profile.first_name, 'hacked')
