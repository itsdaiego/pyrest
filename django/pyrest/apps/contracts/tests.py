from django.test import TestCase
from django.contrib.auth.models import User

from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from pyrest.apps.contracts.models import Contract
from pyrest.apps.profiles.models import Profile



class ContractAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user1 = User.objects.create_user(
            username='client',
            email='client@example.com',
            password='clientpass123'
        )
        self.user2 = User.objects.create_user(
            username='contractor',
            email='contractor@example.com',
            password='contractorpass123'
        )
        
        self.client_profile = Profile.objects.create(
            user=self.user1,
            first_name='Client',
            last_name='User',
            profession='Manager',
            type='client'
        )
        self.contractor_profile = Profile.objects.create(
            user=self.user2,
            first_name='Contractor',
            last_name='User',
            profession='Developer',
            type='contractor'
        )


        self.contract_data = {
            'client_id': self.client_profile.id,
            'contractor_id': self.contractor_profile.id,
        }

        refresh1 = RefreshToken.for_user(self.user1)
        refresh2 = RefreshToken.for_user(self.user2)

        self.client_token = refresh1.access_token
        

    def test_create_contract(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.client_token}')
        response = self.client.post('/api/contracts/', self.contract_data, format='json')

        data = response.json()
        contract = data['contract']

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('message', data)
        self.assertIn('contract', data)
        self.assertEqual(Contract.objects.count(), 1)

        self.assertEqual(contract['client_id'], self.client_profile.id)
        self.assertEqual(contract['contractor_id'], self.contractor_profile.id)

    def test_create_contract_invalid_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.client_token}')
        invalid_data = {
            'client_id': 9999,
            'contractor_id': self.contractor_profile.id,
        }

        response = self.client.post('/api/contracts/', invalid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_contract_same_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.client_token}')
        invalid_data = {
            'client_id': self.client_profile.id,
            'contractor_id': self.client_profile.id,
        }

        response = self.client.post('/api/contracts/', invalid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_crete_contract_unauthorized(self):
        response = self.client.post('/api/contracts/', self.contract_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def tearDown(self):
        User.objects.all().delete()
        Profile.objects.all().delete()
        Contract.objects.all().delete()
