# Generated by Django 3.0.7 on 2020-06-10 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0011_auto_20200510_1239'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='mealtype',
            constraint=models.UniqueConstraint(fields=('name',), name='constraint - unique meal type'),
        ),
        migrations.AddConstraint(
            model_name='menuitem',
            constraint=models.UniqueConstraint(fields=('name', 'meal_type'), name='constraint - unique menu item'),
        ),
        migrations.AddConstraint(
            model_name='topping',
            constraint=models.UniqueConstraint(fields=('name',), name='constraint - unique topping'),
        ),
    ]
