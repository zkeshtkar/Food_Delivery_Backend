# Generated by Django 3.0.8 on 2021-06-22 14:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('managers', '0012_order_restaurant'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='time',
            field=models.TimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]