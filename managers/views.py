from django.db.models import Manager
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from customers.serializers import OrderSerializer
from managers.models import Restaurant, Food, Order
from managers.serializers import RestaurantSerializer, FoodSerializer, \
    OrderDataManagerSerializer


class RestaurantView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RestaurantSerializer

    def post(self, request):
        User.objects.get(id=request.user.id)
        serializer = RestaurantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({'message': 'Car added successfully!'})

        return Response({'message': RestaurantSerializer.errors})

    def put(self, request, restaurant_id):
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)
        restaurant_serializer = RestaurantSerializer(
            instance=restaurant,
            data=request.data,
            partial=True
        )

        if restaurant_serializer.is_valid():
            restaurant_serializer.save()
            return Response({'message': 'Restaurant updated successfully!'})

        return Response({'message': restaurant_serializer.errors})

    def get(self, request):
        queryset = Restaurant.objects.filter(user=request.user)
        serializer = RestaurantSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FoodView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FoodSerializer

    def post(self, request, restaurant_id):
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)
        serializer = FoodSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(restaurant=restaurant)
            return Response({'message': 'Food added successfully!'})

        return Response({'message': RestaurantSerializer.errors})

    def put(self, request, restaurant_id, food_id):
        foods = Food.objects.filter(id=food_id, restaurant__id=restaurant_id)
        if foods is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            for food in foods:
                food.ordered = request.data.get('ordered')
                food.save()
            return Response({'message': 'Food changed successfully!'})

    def delete(self, request, restaurant_id, food_id):
        food = Food.objects.filter(id=food_id, restaurant__id=restaurant_id).delete()
        if food is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:

            return Response({'message': 'Food deleted successfully!'})

    def get(self, request, restaurant_id):
        queryset = Food.objects.filter(restaurant__id=restaurant_id)
        serializer = FoodSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer

    def get(self, request, restaurant_id):
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)
        return Response(dict(message=OrderSerializer.errors, data=restaurant))

    def put(self, request, restaurant_id, order_id):
        order = Order.objects.get(id=order_id)
        if order is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            order.is_accepted = request.data.get('is_accepted')
            order.save()
            return Response({'message': 'Order changed successfully!'})


class OrderView2(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer

    def get(self, request):
        restaurant = Restaurant.objects.filter(user__id=request.user.id)
        orders = Order.objects.filter(restaurant__id=restaurant[0].id)
        serializer = OrderDataManagerSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FoodOrder(APIView):
    def get(self, request, order_id):
        orders = Food.objects.filter(order__id=order_id)
        serializer = FoodSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
