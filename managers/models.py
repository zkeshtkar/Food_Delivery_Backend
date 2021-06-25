from django.contrib.postgres.fields import ArrayField
from django.db import models

from accounts.models import User
from customers.models import Customer


class Restaurant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.TimeField(auto_now=False, auto_now_add=False)
    end_time = models.TimeField(auto_now=False, auto_now_add=False)
    name = models.CharField(max_length=60, unique=True)
    address = models.CharField(null=True, max_length=600)
    food_delivery_time = models.TimeField(auto_now=False, auto_now_add=False)
    fixed_cost = models.IntegerField(default=0)
    area_service = ArrayField(models.IntegerField(), blank=True)
    region = models.SmallIntegerField(default=0)


class Food(models.Model):
    name = models.CharField(max_length=60, null=False)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, default=None)
    price = models.IntegerField(default=0)
    ordered = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        WAITING = 'W', 'Waiting'
        PREPARING = 'P', 'Preparing'
        SENDING = 'S', 'Sending'
        DONE = 'D', 'Done'

    state = models.CharField(
        max_length=1,
        default=OrderStatus.WAITING,
        choices=OrderStatus.choices,
    )
    is_accepted = models.BooleanField(default=False)
    price = models.IntegerField(default=0)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, default=None)
    foods = models.ManyToManyField(Food, default=None)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, default=None)
    start = models.TimeField(auto_now_add=True)
    now = models.TimeField(auto_now=True)


class Comment(models.Model):
    score = models.IntegerField(default=0)
    text = models.TextField(null=True, max_length=140)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, default=None)
