from datetime import datetime

from django.db import transaction
from django.db.models import Avg
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import exceptions

from accounts.permissions import IsCustomer
from customers.models import Customer
from customers.serializers import CustomerSerializer, OrderSerializer, \
    CommentSerializer
from managers.models import Restaurant, Food, Order, Comment
from managers.serializers import FoodSerializer


class CustomerView(APIView):
    """
    update profile for customer user and get profile
    """
    permission_classes = (IsCustomer,)
    serializer_class = CustomerSerializer

    def post(self, request):
        try:
            customer = Customer.objects.get(user=request.user)
            serialized_data = self.serializer_class(data=request.data, instance=customer, partial=True)
            if serialized_data.is_valid(raise_exception=True):
                serialized_data.save()
                return Response(status=status.HTTP_200_OK)
        except exceptions.ValidationError as e:
            return Response(status=e.status_code)

        except Customer.DoesNotExist as e:
            return Response(status=e.status_code)

    def get(self, request):
        try:
            customer = Customer.objects.get(user__id=request.user.id)
        except Customer.DoesNotExist as e:
            return Response(status=e.status_code)
        return Response(data=self.serializer_class(customer).data, status=status.HTTP_200_OK)


class OrderView(APIView):
    """
    order foods by food_id and get them
    """
    permission_classes = (IsCustomer,)
    serializer_class = OrderSerializer

    @transaction.atomic
    def post(self, request, restaurant_name):
        restaurant = get_object_or_404(Restaurant, name=restaurant_name)
        foods_id = request.data.get('foods')
        customer = Customer.objects.get(user__id=request.user.id)
        price = 0
        for food_id in foods_id:
            food = Food.objects.get(id=int(food_id))
            price += food.price
            if customer.credit < price or not food.ordered:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        price += restaurant.fixed_cost
        if customer.credit < price:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        order = Order.objects.create(user=customer, restaurant=restaurant, is_accepted=False)
        order.price = price
        order.foods.add(*foods_id)
        order.save()
        customer.credit = customer.credit - price
        customer.save()
        return Response({'message': 'order added successfully!'})

    def get(self, request):
        try:
            customer = Customer.objects.get(user__id=request.user.id)
            orders = Order.objects.filter(user__id=customer.id)
            return Response(data=self.serializer_class(orders, many=True).data, status=status.HTTP_200_OK)
        except Customer.DoesNotExist as e:
            return Response(status=e.status_code)


class FoodSearch(APIView):
    """
    search foods by name of restaurant or region or name of food
    """
    permission_classes = (IsCustomer,)
    serializer_class = FoodSerializer

    def get(self, request, search_type, name):
        now = datetime.now()
        if search_type == 'food':
            queryset = Food.objects.filter(name=name, ordered=True)
        elif search_type == 'restaurant':
            queryset = Food.objects.filter(restaurant__name=name, ordered=True)
        elif search_type == 'region':
            queryset = Food.objects.filter(restaurant__area_service__contains=[int(name)], ordered=True)
        else:
            queryset = Food.objects.filter(ordered=True, restaurant__start_time__lt=now,
                                           restaurant__end_time__gt=now)
        return Response(data=self.serializer_class(queryset, many=True).data, status=status.HTTP_200_OK)


class FoodOrder(APIView):
    """
    get food by order id
    """
    permission_classes = (IsCustomer,)
    serializer_class = FoodSerializer

    def get(self, request, order_id):
        orders = Food.objects.filter(order__id=order_id)
        return Response(self.serializer_class(orders, many=True).data, status=status.HTTP_200_OK)


class CommentView(APIView):
    """
    add comment for food by food_id
    """
    permission_classes = (IsCustomer,)
    serializer_class = CommentSerializer

    def post(self, request, food_id):
        try:

            food = Food.objects.get(id=food_id)
            user = Customer.objects.get(user__id=request.user.id)
            serialized_data = self.serializer_class(data=request.data)
            if serialized_data.is_valid(raise_exception=True):
                serialized_data.save(food=food, user=user)
                return Response(status=status.HTTP_200_OK)
        except exceptions.ValidationError as e:
            return Response(status=e.status_code)
        except Food.DoesNotExist as e:
            return Response(status=e.status_code)
        except Customer.DoesNotExist as e:
            return Response(status=e.status_code)

        return Response({'message': CommentSerializer.errors})


class FavoriteFoodView(APIView):
    """
    get favorite food
    """
    permission_classes = (IsCustomer,)
    serializer_class = FoodSerializer

    def get(self, request):
        try:
            customer = Customer.objects.get(user__id=request.user.id)
            favorite_foods = Comment.objects.filter(
                user__id=customer.id
            ).values_list(
                'score'
            ).order_by(
                'score'
            ).annotate(
                avg_score=Avg('score')
            ).filter(
                avg_score__gt=3
            )
            return Response(self.serializer_class(favorite_foods, many=True).data, status=status.HTTP_200_OK)
        except Customer.DoesNotExist as e:
            return Response(status=e.status_code)
