from rest_framework import status, exceptions
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from customers.serializers import OrderSerializer
from accounts.permissions import IsManager
from managers.models import Restaurant, Food, Order
from managers.serializers import RestaurantSerializer, FoodSerializer


class RestaurantView(APIView):
    permission_classes = (IsManager,)
    serializer_class = RestaurantSerializer
    """
    Add restaurant and update it
    """

    def post(self, request):
        try:
            user = User.objects.get(id=request.user.id)
            serialized_data = self.serializer_class(data=request.data)
            if serialized_data.is_valid(raise_exception=True):
                serialized_data.save(user=user)
                return Response(status=status.HTTP_200_OK)
        except exceptions.ValidationError as e:
            return Response(status=e.status_code)
        except User.DoesNotExist as e:
            return Response(status=e.status_code)

    def put(self, request, restaurant_id):
        try:
            restaurant = Restaurant.objects.get(id=restaurant_id)
            serialized_data = self.serializer_class(instance=restaurant, data=request.data, partial=True)

            if serialized_data.is_valid(raise_exception=True):
                serialized_data.save()
                return Response(status=status.HTTP_200_OK)
        except exceptions.ValidationError as e:
            return Response(status=e.status_code)
        except Restaurant.DoesNotExist as e:
            return Response(status=e.status_code)

    def get(self, request):
        queryset = Restaurant.objects.filter(user=request.user)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FoodView(APIView):
    permission_classes = (IsManager,)
    serializer_class = FoodSerializer

    def post(self, request, restaurant_id):
        try:
            restaurant = Restaurant.objects.get(id=restaurant_id)
            serialized_data = self.serializer_class(data=request.data)
            if serialized_data.is_valid(raise_exception=True):
                serialized_data.save(restaurant=restaurant)
                return Response(status=status.HTTP_200_OK)
        except exceptions.ValidationError as e:
            return Response(status=e.status_code)
        except Restaurant.DoesNotExist as e:
            return Response(status=e.status_code)

    def put(self, request, food_id):
        try:
            food = Food.objects.get(id=food_id)
            serialized_data = self.serializer_class(data=request.data, instance=food, partial=True)
            if serialized_data.is_valid(raise_exception=True):
                serialized_data.save()
                return Response(status=status.HTTP_200_OK)
        except exceptions.ValidationError as e:
            return Response(status=e.status_code)
        except Food.DoesNotExist as e:
            return Response(status=e.status_code)

    def delete(self, request, restaurant_id, food_id):

        try:
            Food.objects.get(id=food_id, restaurant__id=restaurant_id).delete()
            return Response(status=status.HTTP_200_OK)
        except Food.DoesNotExist as e:
            return Response(status=e.status_code)

    def get(self, request, restaurant_id):
        try:
            food = Food.objects.get(restaurant__id=restaurant_id)
            serialized_data = self.serializer_class(food, many=True)
            return Response(serialized_data.data, status=status.HTTP_200_OK)
        except Food.DoesNotExist as e:
            return Response(status=e.status_code)


class OrderView(APIView):
    permission_classes = (IsManager,)
    serializer_class = OrderSerializer

    def get(self, request):
        try:
            restaurant = Restaurant.objects.get(user__id=request.user.id)
            serialized_data = self.serializer_class(restaurant, many=True)
            return Response(serialized_data.data, status=status.HTTP_200_OK)
        except Restaurant.DoesNotExist as e:
            return Response(status=e.status_code)

    def put(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
            serialized_data = self.serializer_class(data=request.data, instance=order, partial=True)
            if serialized_data.is_valid(raise_exception=True):
                serialized_data.save()
                return Response(status=status.HTTP_200_OK)
        except exceptions.ValidationError as e:
            return Response(status=e.status_code)
        except Order.DoesNotExist as e:
            return Response(status=e.status_code)


class FoodOrder(APIView):
    permission_classes = (IsManager,)
    serializer_class = FoodSerializer

    def get(self, request, order_id):
        try:
            food = Food.objects.get(orderd__id=order_id)
            serialized_data = self.serializer_class(food, many=True)
            return Response(serialized_data.data, status=status.HTTP_200_OK)
        except Food.DoesNotExist as e:
            return Response(status=e.status_code)
