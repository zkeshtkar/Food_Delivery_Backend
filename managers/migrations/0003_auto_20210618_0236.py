# Generated by Django 3.0.8 on 2021-06-18 02:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('managers', '0002_auto_20210617_1949'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='food',
            name='restaurant',
        ),
        migrations.AddField(
            model_name='food',
            name='restaurant',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='managers.Restaurant'),
        ),
    ]
