# Generated by Django 3.0.8 on 2021-06-22 12:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('managers', '0009_order_restaurant'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='restaurant',
        ),
    ]
