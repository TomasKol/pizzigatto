# Generated by Django 3.0.3 on 2020-04-23 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0005_mealtype_is_available'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='image',
            field=models.ImageField(blank=True, default='default_item.png', upload_to=''),
        ),
    ]
