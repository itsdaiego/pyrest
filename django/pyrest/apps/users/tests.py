from django.db import connection
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status

from pyrest.apps.profiles.models import Profile


class UserAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'password2': 'newpass123'
        }

    def test_create_user_api(self):
        response = self.client.post('/api/users', self.user_data, format='json')
        data = response.json()
        user = User.objects.get(username='newuser')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(user.get_username(), 'newuser')
        self.assertIn('message', data)
        self.assertIn('user', data)

    def test_login_user(self):
        User.objects.create_user(username='newuser', email='newuser@example.com', password='newpass123')
        response = self.client.post('/api/login/', {
            'username': 'newuser',
            'password': 'newpass123'
        }, format='json')
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', data)
        self.assertIn('refresh', data)
        self.assertIn('user', data)

    def test_register_user(self):
        response = self.client.post('/api/register/', self.user_data, format='json')
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'newuser')
        self.assertIn('message', data)
        self.assertIn('user', data)

    def test_register_user_password_mismatch(self):
        self.user_data['password2'] = 'mismatchedpassword'
        response = self.client.post('/api/register/', self.user_data, format='json')
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', data)

    def test_login_user_invalid_credentials(self):
        response = self.client.post('/api/login/', {
            'username': 'nonexistentuser',
            'password': 'wrongpassword'
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def tearDown(self):
        User.objects.all().delete()
        Profile.objects.all().delete()

