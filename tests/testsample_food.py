import json

from django.test import TestCase, Client
from accounts.models import User
from customers.models import Customer
from managers.models import Restaurant, Manager, Food


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

        url = '/manager/add/restaurant'
        header = self.login_manager()
        data = {
            'name': 'مروارید', 'start_time': '14:22', 'end_time': '14:22', 'address': 'مرزداران',
            'food_delivery_time': '14:22', 'fixed_cost': '1000', 'region': '2', 'area_service': [1]

        }
        self.client.post(url, data=data, format='json', **header)
        self.restaurant = Restaurant.objects.get(manager__user=self.manager)

    def test_sample_manager_food(self):
        header = self.login_manager()
        url = '/manager/add/food/' + str(self.restaurant.id)
        data = {
            'name': 'کباب',
            'price': '1000',
            'ordered': 'True'

        }
        self.client.post(url, data=data, format='json', **header)
        food = Food.objects.get(restaurant__id=self.restaurant.id)
        self.assertEqual(food.name, "کباب")
        self.assertEqual(food.price, 1000)
        self.assertEqual(food.ordered, True)

        url = '/manager/update/food/' + str(food.id)
        data = {'name': 'کتلت'}
        self.client.put(url
                        , data=json.dumps(data), content_type='application/json', **header)
        food = Food.objects.get(restaurant__id=self.restaurant.id)
        self.assertEqual(food.name, "کتلت")
        self.assertEqual(food.price, 1000)
        self.assertEqual(food.ordered, True)

        foods = Food.objects.filter(restaurant__id=self.restaurant.id)
        self.assertEqual(len(foods), 1)

        url = '/manager/foods/' + str(self.restaurant.id)
        response = self.client.get(url, **header)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0].get('price'), 1000)
        self.assertEqual(response.data[0].get('ordered'), 'بله')

        url = '/manager/delete/food/' + str(food.id)
        self.client.delete(url, **header)
        foods = Food.objects.filter(restaurant__id=self.restaurant.id)
        self.assertEqual(len(foods), 0)

    def test_sample_customer_Search_food(self):
        header = self.login_manager()
        url = '/manager/add/food/' + str(self.restaurant.id)
        data = {
            'name': 'کباب',
            'price': '1000',
            'ordered': 'True'

        }
        self.client.post(url, data=data, format='json', **header)

        url = '/customer/search/restaurant/مروارید'
        header = self.login_customer()

        response = self.client.get(url, **header)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0].get('price'), 1000)

        url = '/customer/search/restaurant/تجریش'
        response = self.client.get(url, **header)
        self.assertEqual(len(response.data), 0)

        url = '/customer/search/food/کباب'
        response = self.client.get(url, **header)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0].get('price'), 1000)

        url = '/customer/search/food/قیمه'
        response = self.client.get(url, **header)
        self.assertEqual(len(response.data), 0)

        url = '/customer/search/region/8'
        response = self.client.get(url, **header)
        self.assertEqual(len(response.data), 0)

        url = '/customer/search/region/1'
        response = self.client.get(url, **header)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0].get('price'), 1000)
