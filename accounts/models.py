from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import phone_validator, EmailValidator


class User(AbstractUser):
    phone = models.CharField(max_length=15, validators=[phone_validator], blank=True)
    email = models.EmailField(max_length=50, validators=[EmailValidator], blank=True)

    @property
    def is_manager(self):
        return hasattr(self, 'manager')

    @property
    def is_customer(self):
        return hasattr(self, 'customer')
