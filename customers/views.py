import time
from datetime import datetime

from django.db.models import Avg
from rest_framework import status, generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import exceptions

from accounts.models import User
from customers import transactions
from customers.models import Customer
from customers.serializers import CustomerSerializer, OrderSerializer, ProfileDataSerializer, \
    CommentSerializer
from managers.models import Restaurant, Food, Order, Comment
from managers.serializers import FoodSerializer
from utilities import responses



class CustomerUpdateProfile(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CustomerSerializer

    def post(self, request):
        try:
            serialized_data = self.serializer_class(data=request.data)
            if serialized_data.is_valid(raise_exception=True):
                try:
                    Customer.objects.get(user=request.user)
                except Customer.DoesNotExist as e:
                    return responses.ErrorResponse(message=e.detail, status=e.status_code).send()

                serialized_data.save(user=request.user)
        except exceptions.ValidationError as e:
            return responses.ErrorResponse(message=e.detail, status=e.status_code).send()

        return responses.SuccessResponse(status=status.HTTP_201_CREATED)

    def get(self, request):
        try:
            customer = Customer.objects.get(user__id=request.user.id)
        except Customer.DoesNotExist as e:
            return responses.ErrorResponse(message=e.detail, status=e.status_code).send()
        return Response(ProfileDataSerializer(customer).data)


class OrderView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer

    def post(self, request, restaurant_name):
        print(request.data)
        print(request.user.id)
        print("idddddddddd")
        restaurant = get_object_or_404(Restaurant, name=restaurant_name)
        ids = request.data.get('foods')
        customer = Customer.objects.get(user__id=request.user.id)
        order = Order.objects.create(user=customer, restaurant=restaurant)
        price = 0
        for id in ids:
            food = Food.objects.filter(id=int(id))
            price += food[0].price
            print(food[0].name)
            order.foods.add(food[0])
        order.price = price
        order.save()
        if customer.credit < price:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        customer.credit = customer.credit - price
        customer.save()
        return Response({'message': 'order added successfully!'})

    def get(self, request):
        customer = Customer.objects.get(user__id=request.user.id)
        orders = Order.objects.filter(user__id=customer.id)
        for order in orders:
            if order.is_accepted:
                if order.state == Order.OrderStatus.WAITING:
                    order.state = Order.OrderStatus.PREPARING
                elif order.state == Order.OrderStatus.PREPARING:
                    order.state = Order.OrderStatus.SENDING
                elif order.state == order.OrderStatus.SENDING:
                    order.state = Order.OrderStatus.DONE
                order.save()
        serializer = OrderDataSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FoodSearch(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, search_type, name):
        now = datetime.now()
        if search_type == 'food':
            queryset = Food.objects.filter(name=name, ordered=True)
        elif search_type == 'restaurant':
            queryset = Food.objects.filter(restaurant__name=name, ordered=True)
        elif search_type == 'region':
            arr = [int(name)]
            queryset = Food.objects.filter(restaurant__area_service__contains=arr, ordered=True)
        else:

            queryset = Food.objects.filter(ordered=True, restaurant__start_time__lt=now,
                                           restaurant__end_time__gt=now)
        serializer = FoodDataSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FoodOrder(APIView):
    def get(self, request, order_id):
        orders = Food.objects.filter(order__id=order_id)
        serializer = FoodDataSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentSerializer

    def post(self, request, food_id):
        food = get_object_or_404(Food, id=food_id)
        user = Customer.objects.get(user__id=request.user.id)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(food=food, user=user)
            return Response({'message': 'Food added successfully!'})

        return Response({'message': CommentSerializer.errors})


class FavoriteFoodView(APIView):
    def get(self, request):
        customer = Customer.objects.get(user__id=request.user.id)
        comments = Comment.objects.filter(user__id=customer.id)
        foodlist = []
        for comment in comments:
            for comment2 in comments:
                score = 0
                i = 0
                j = 0
                if comment.food.name == comment2.food.name and comment.food.restaurant.name == comment2.food.restaurant.name:
                    score += comment.score
                    j += 1
                i += 1
                if score != 0 and score / j > 3:
                    foodlist.append(comment.food)
                elif j > 5:
                    foodlist.append(comment.food)
        serializer = FoodDataSerializer(foodlist, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
