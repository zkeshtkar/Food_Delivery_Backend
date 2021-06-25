from datetime import datetime

from rest_framework import serializers

from managers.models import Restaurant, Food


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant

        fields = (
            'address', 'name', 'start_time', 'end_time', 'food_delivery_time', 'fixed_cost',
            'area_service', 'region')

    def create(self, validated_data):
        restaurant = Restaurant.objects.create(**validated_data)

        restaurant.save()

        return restaurant

    def update(self, instance, validated_data):
        instance.start_time = validated_data.get(
            'start_time', instance.start_time
        )
        instance.end_time = validated_data.get(
            'end_time', instance.end_time
        )
        instance.name = validated_data.get(
            'name', instance.name
        )
        instance.address = validated_data.get(
            'address', instance.address
        )
        instance.food_delivery_time = validated_data.get(
            'food_delivery_time', instance.food_delivery_time
        )
        instance.fixed_cost = validated_data.get(
            'fixed_cost', instance.fixed_cost
        )
        instance.fixed_cost = validated_data.get(
            'fixed_cost', instance.fixed_cost
        )
        # instance.area_service = validated_data.get(
        #     validated_data.pop('area_service'), instance.area_service
        # )
        print(validated_data)
        print("~~~~~~~~~~~~~~")

        instance.save()
        return instance

    def to_representation(self, instance):
        return {
            'name': instance.name,
            'address': instance.address,
            'start_time': instance.start_time,
            'end_time': instance.end_time,
            'food_delivery_time': instance.food_delivery_time,
            'fixed_cost': instance.fixed_cost,
            'area_service': instance.area_service,
            'region': instance.region,
            'id': instance.id
        }


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = (
            'name', 'price')

    def create(self, validated_data):

        food = Food.objects.create(**validated_data)

        food.save()
        return food

    def update(self, instance, validated_data):
        instance.start_time = validated_data.get(
            'start_time', instance.start_time
        )
        instance.end_time = validated_data.get(
            'end_time', instance.end_time
        )
        instance.name = validated_data.get(
            'name', instance.name
        )
        instance.address = validated_data.get(
            'address', instance.address
        )
        instance.food_delivery_time = validated_data.get(
            'food_delivery_time', instance.food_delivery_time
        )
        instance.fixed_cost = validated_data.get(
            'fixed_cost', instance.fixed_cost
        )
        instance.fixed_cost = validated_data.get(
            'fixed_cost', instance.fixed_cost
        )
        instance.area_service = validated_data.get(
            validated_data.pop('area_service'), instance.area_service
        )

        instance.save()
        return instance

    def to_representation(self, instance):
        if instance.ordered:
            ans = 'بله'
        else:
            ans = 'خیر'

        return {
            'name': instance.name,
            'price': instance.price,
            'ordered': ans,
            'id': instance.id,
            'ordered2': instance.ordered,
            'restaurant': instance.restaurant.name

        }


class OrderDataManagerSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        state = ''
        if instance.state == 'W':
            state = 'در حال انتظار'
        elif instance.state == 'P':
            state = 'در حال اماده سازی'
        elif instance.state == 'S':
            state = 'در حال ارسال'
        else:
            state = 'دریافت شده'
        return {
            'price': instance.price,
            'restaurant': instance.restaurant.name,
            'id': instance.id,
            'state': state,
            'username': instance.user.name
        }
