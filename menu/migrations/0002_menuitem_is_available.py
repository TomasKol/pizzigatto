# Generated by Django 3.0.3 on 2020-04-22 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='is_available',
            field=models.BooleanField(default=True),
        ),
    ]
