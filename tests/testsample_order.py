import json

from django.test import TestCase, Client
from accounts.models import User
from customers.models import Customer
from managers.models import Restaurant, Manager, Food, Order


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
        Manager.objects.get(user__username="zkeshtkarzzz@gmail.com")
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

        url = '/manager/add/restaurant'
        header = self.login_manager()
        data = {
            'name': 'مروارید', 'start_time': '14:22', 'end_time': '14:22', 'address': 'مرزداران',
            'food_delivery_time': '14:22', 'fixed_cost': '1000', 'region': '2', 'area_service': [1]

        }
        self.client.post(url, data=data, format='json', **header)
        self.restaurant = Restaurant.objects.get(manager__user=self.manager)

        url = '/manager/add/food/' + str(self.restaurant.id)
        data = {
            'name': 'کباب',
            'price': '1000',
            'ordered': 'True'

        }
        header = self.login_manager()
        self.client.post(url, data=data, format='json', **header)
        self.food1 = Food.objects.get(restaurant__id=self.restaurant.id)

        url = '/manager/add/food/' + str(self.restaurant.id)
        data = {
            'name': 'کتلت',
            'price': '1000',
            'ordered': 'False'

        }
        header = self.login_manager()
        self.client.post(url, data=data, format='json', **header)
        foods = Food.objects.filter(restaurant__id=self.restaurant.id)
        self.food1 = foods[0]
        self.food2 = foods[1]

    def test_sample_customer_order(self):
        header = self.login_customer()
        url = '/customer/add/order/' + str(self.restaurant.name)
        data = {
            'foods': [
                self.food2.id
            ]

        }
        response = self.client.post(url, data=data, format='json', **header)
        self.assertEqual(response.status_code, 400)

        url = '/customer/add/order/' + str(self.restaurant.name)
        data = {
            'foods': [
                self.food1.id
            ]

        }

        self.client.post(url, data=data, format='json', **header)
        order = Order.objects.get(user__user__id=self.customer.id)
        self.assertEqual(order.is_accepted, False)
        self.assertEqual(order.price, 2000)
        self.assertEqual(len(order.foods.all()), 1)
        self.assertEqual(order.foods.all()[0], self.food1)

        url = '/customer/orders'
        customer = Customer.objects.get(user=self.customer)
        response = self.client.get(url, **header)
        self.assertEqual(response.data[0].get('price'), 2000)
        self.assertEqual(response.data[0].get('restaurant'), self.restaurant.name)
        self.assertEqual(response.data[0].get('state'), 'در حال انتظار')
        self.assertEqual(response.data[0].get('username'), customer.name)

        url = '/customer/food/order/' + str(order.id)
        response = self.client.get(url, **header)
        self.assertEqual(response.data[0].get('price'), 1000)
        self.assertEqual(response.data[0].get('restaurant'), self.restaurant.name)
        self.assertEqual(response.data[0].get('name'), 'کباب')

    def test_sample_manager_order(self):
        header = self.login_customer()
        header_manager = self.login_manager()
        url = '/customer/add/order/' + str(self.restaurant.name)
        data = {
            'foods': [
                self.food1.id
            ]

        }

        self.client.post(url, data=data, format='json', **header)
        order = Order.objects.get(user__user__id=self.customer.id)

        url = '/manager/get/orders/' + str(self.restaurant.id)
        response = self.client.get(url, **header_manager)
        self.assertEqual(response.data[0].get('price'), order.price)
        self.assertEqual(response.data[0].get('restaurant'), order.restaurant.name)
        self.assertEqual(response.data[0].get('state'), 'در حال انتظار')
        self.assertEqual(response.data[0].get('username'), order.user.name)
        self.assertEqual(response.data[0].get('is_accepted'), False)

        url = '/manager/update/order/' + str(order.id)
        data = {'is_accepted': 'True'}
        self.client.put(url
                        , data=json.dumps(data), content_type='application/json', **header_manager)

        order = Order.objects.get(user__user__id=self.customer.id)
        self.assertEqual(order.is_accepted, True)
