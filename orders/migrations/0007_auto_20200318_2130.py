# Generated by Django 3.0.3 on 2020-03-18 20:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_auto_20200318_1509'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='extraCheese',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='pizzaToppings',
        ),
    ]
