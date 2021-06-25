from django.contrib.auth import authenticate
from django.db import transaction

from accounts.models import User
from customers.models import Customer


@transaction.atomic
def register_user_with_email_and_password(email, password):
    user = User.objects.create_user(email=email, username=email, password=password)
    user.save()
    return user


@transaction.atomic
def register_user_with_phone_and_password(phone, password):
    user = User.objects.create_user(username=phone, password=password, phone=phone)
    user.save()
    customer = Customer.objects.create(user=user)
    customer.save()
    return user
