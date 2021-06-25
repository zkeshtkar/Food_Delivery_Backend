from rest_framework import serializers

from managers.models import Order, Food, Comment
from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = (
            'name', 'address', 'region')

    def to_representation(self, instance):
        return {
            'name': instance.name,
            'address': instance.address,
            'region': instance.region,
            'credit': instance.credit
        }

    def create(self, validated_data):
        customer = Customer.objects.create(**validated_data)
        customer.save()

    def update(self, instance, validated_data):
        instance.name = validated_data.get(
            'name', instance.name
        )
        instance.address = validated_data.get(
            'address', instance.address
        )
        instance.region = validated_data.get(
            'region', instance.region
        )
        instance.save()
        return instance


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        order = Order.objects.create(**validated_data)
        order.save()
        foods_data = validated_data.pop('foods')
        for food_data in foods_data:
            Food.objects.create(order=order, **food_data)
        return order

    def to_representation(self, instance):
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


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            'score', 'text')

    def create(self, validated_data):
        comment = Comment.objects.create(**validated_data)

        comment.save()
        return comment
