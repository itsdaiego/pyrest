from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()

class UserModelTests(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass123'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'testuser@example.com')
        self.assertTrue(user.check_password('testpass123'))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        self.assertEqual(admin_user.username, 'admin')
        self.assertEqual(admin_user.email, 'admin@example.com')
        self.assertTrue(admin_user.check_password('adminpass123'))
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

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
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'newuser')
        self.assertIn('message', response.data)
        self.assertIn('user', response.data)

    def test_login_user(self):
        User.objects.create_user(username='newuser', email='newuser@example.com', password='newpass123')
        response = self.client.post('/api/login/', {
            'username': 'newuser',
            'password': 'newpass123'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user', response.data)

    def test_register_user(self):
        response = self.client.post('/api/register/', self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'newuser')
        self.assertIn('message', response.data)
        self.assertIn('user', response.data)

    def test_register_user_password_mismatch(self):
        self.user_data['password2'] = 'mismatchedpassword'
        response = self.client.post('/api/register/', self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_login_user_invalid_credentials(self):
        response = self.client.post('/api/login/', {
            'username': 'nonexistentuser',
            'password': 'wrongpassword'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)