from django.db import models

from accounts.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(null=True, max_length=50)
    address = models.TextField(null=True)
    region = models.SmallIntegerField(default=0)
    credit = models.IntegerField(default=1000_000)

    def __str__(self):
        return self.name


