import json

from django.test import TestCase, Client
from accounts.models import User
from customers.models import Customer
from managers.models import Restaurant, Manager


class TestAll(TestCase):
    def login_customer(self):
        login_response = self.client.post('/accounts/login', data={
            "username": "09301094455",
            "password": "123Aa123"
        }, format='json')
        self.assertEqual(200, login_response.status_code)
        token = login_response.data['token']
        token = 'Token ' + token
        header = {'HTTP_AUTHORIZATION': token}
        return header

    def login_manager(self):
        login_response = self.client.post('/accounts/login', data={
            "username": "zkeshtkarzzz@gmail.com",
            "password": "123Aa123"
        }, format='json')
        self.assertEqual(200, login_response.status_code)
        token = login_response.data['token']
        token = 'Token ' + token
        header = {'HTTP_AUTHORIZATION': token}
        manager = Manager.objects.get(user__username="zkeshtkarzzz@gmail.com")
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

        url = '/accounts/register/manager'
        data = {
            "password": "123Aa123",
            "email": "zkeshtkarzzz@gmail.com"
        }
        self.client.post(url, data=data, format='json')
        self.manager = User.objects.get(username="zkeshtkarzzz@gmail.com")

    def test_sample_customer_complete_registration(self):
        header = self.login_customer()
        url = '/customer/update/profile'
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
        url = '/customer/update/profile'
        data = {
            "name": "zahra",
            "region": "5"
        }
        self.client.post(url, data=data, format='json', **header)
        customer = Customer.objects.get(user=self.customer)
        self.assertEqual(customer.user, self.customer)
        self.assertEqual(customer.name, "zahra")
        self.assertEqual(customer.address, None)

        url = '/customer/profile'
        response = self.client.get(url, format='json', **header)
        self.assertEqual(customer.name, response.data.get('name'))
        self.assertEqual(customer.address, response.data.get('address'))
        self.assertEqual(customer.credit, response.data.get('credit'))

    def test_sample_manager_add_restaurant(self):
        header = self.login_manager()
        url = '/manager/add/restaurant'
        data = {
            'name': 'مروارید', 'start_time': '14:22', 'end_time': '14:22', 'address': 'مرزداران',
            'food_delivery_time': '14:22', 'fixed_cost': '1000', 'region': '2', 'area_service': [1]

        }
        self.client.post(url, data=data, format='json', **header)
        restaurant = Restaurant.objects.get(manager__user__id=self.manager.id)
        self.assertEqual(restaurant.manager.user, self.manager)
        self.assertEqual(restaurant.name, "مروارید")
        self.assertEqual(restaurant.address, "مرزداران")
        self.assertEqual(restaurant.fixed_cost, 1000)
        self.assertEqual(restaurant.area_service, [1])
        url = '/manager/update/restaurant/' + str(restaurant.id)
        data = {'name': 'sib'}
        self.client.put(url
                        , data=json.dumps(data), content_type='application/json', **header)
        restaurant = Restaurant.objects.get(manager__user__id=self.manager.id)
        self.assertEqual(restaurant.name, "sib")
        self.assertEqual(restaurant.address, "مرزداران")

        url = '/manager/restaurants'
        response = self.client.get(url, **header)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0].get('name'), "sib")
        self.assertEqual(response.data[0].get('address'), "مرزداران")

