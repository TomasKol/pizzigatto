# Generated by Django 3.0.3 on 2020-03-20 12:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0013_auto_20200320_1315'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartitem',
            old_name='priceUnit',
            new_name='price',
        ),
    ]
