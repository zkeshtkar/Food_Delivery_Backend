from datetime import datetime

from django.test import TestCase, Client
from accounts.models import User
from customers.models import Customer


class TestAll(TestCase):
    def login_customer(self):
        login_response = self.client.post('/accounts/login/', data={
            "username": "09301094455",
            "password": "123Aa123"
        }, format='json')
        self.assertEqual(200, login_response.status_code)
        token = login_response.data['token']
        token = 'Token ' + token
        header = {'HTTP_AUTHORIZATION': token}
        return header

    def setUp(self):
        self.client = Client()
        url = '/accounts/register/customer'
        data = {
            "password": "123Aa123",
            "phone": "09301094455"
        }
        self.client.post(url, data=data, format='json')
        self.customer = User.objects.get(username="09301094455")

    def test_sample_customer_complete_registration(self):
        header = self.login_customer()
        url = '/customer/update/profile/'
        data = {
            "name": "zahra",
            "region": "5",
            "address": "Tehran"
        }
        self.client.post(url, data, format='json', **header)
        customer = Customer.objects.get(user=self.customer)
        self.assertEqual(customer.user, self.customer)
        self.assertEqual(customer.name, "zahra")
        self.assertEqual(customer.address, "Tehran")

    def test_sample_customer_with_no_address_registration(self):
        header = self.login_customer()
        url = '/customer/update/profile/'
        data = {
            "name": "zahra",
            "region": "5"
        }
        self.client.post(url, data=data, format='json', **header)
        customer = Customer.objects.get(user=self.customer)
        self.assertEqual(customer.user, self.customer)
        self.assertEqual(customer.name, "zahra")
        self.assertEqual(customer.address, None)

