from django.test import TestCase
from django.contrib.auth.models import User

from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from pyrest.apps.contracts.models import Contract
from pyrest.apps.profiles.models import Profile
from pyrest.apps.jobs.models import Job


class JobAPITests(TestCase):
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
            type='client',
            balance=1000
        )
        self.contractor_profile = Profile.objects.create(
            user=self.user2,
            first_name='Contractor',
            last_name='User',
            profession='Developer',
            type='contractor',
            balance=0
        )

        self.contract = Contract.objects.create(
            client=self.client_profile,
            contractor=self.contractor_profile
        )

        self.job_data = {
            'description': 'Test job',
            'price': 1000,
            'paid': False,
            'payment_date': '2024-10-10T12:00:00Z',
            'contract_id': self.contract.id
        }

        refresh = RefreshToken.for_user(self.user1)
        self.client_token = refresh.access_token

        refresh2 = RefreshToken.for_user(self.user2)
        self.contractor_token = refresh2.access_token

    def test_create_job(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.client_token}')
        response = self.client.post('/api/jobs/', self.job_data, format='json')

        data = response.json()
        job = data['job']

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('message', data)
        self.assertIn('job', data)
        self.assertEqual(Job.objects.count(), 1)

        self.assertEqual(job['description'], self.job_data['description'])
        self.assertEqual(job['price'], self.job_data['price'])
        self.assertEqual(job['paid'], self.job_data['paid'])
        self.assertEqual(job['payment_date'], self.job_data['payment_date'])
        self.assertEqual(job['contract_id'], self.job_data['contract_id'])

    def test_create_job_invalid_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.client_token}')
        invalid_data = {
            'description': 'Test job',
            'price': 'not a number',
            'paid': False,
            'payment_date': '2024-10-10T12:00:00Z',
            'contract_id': self.contract.id
        }

        response = self.client.post('/api/jobs/', invalid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_job_non_existent_contract(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.client_token}')
        invalid_data = {
            'description': 'Test job',
            'price': 1000,
            'paid': False,
            'payment_date': '2024-10-10T12:00:00Z',
            'contract_id': 9999
        }

        response = self.client.post('/api/jobs/', invalid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_perform_payment(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.client_token}')
        job = Job.objects.create(**self.job_data)

        response = self.client.post(f'/api/jobs/{job.id}/pay/', format='json')
        data = response.json()
        paid_job = data['job']

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', data)
        self.assertIn('job', data)

        self.assertEqual(paid_job['description'], job.description)
        self.assertEqual(paid_job['price'], job.price)
        self.assertEqual(paid_job['paid'], True)

        client = Profile.objects.get(user=self.user1)
        contractor = Profile.objects.get(user=self.user2)

        self.assertEqual(client.balance, 0)
        self.assertEqual(contractor.balance, 1000)


    def test_perform_payment_unauthorized(self):
        response = self.client.post('/api/jobs/', self.job_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def tearDown(self):
        User.objects.all().delete()
        Profile.objects.all().delete()
        Contract.objects.all().delete()
        Job.objects.all().delete()
