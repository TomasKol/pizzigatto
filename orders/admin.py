from django.contrib import admin
from .models import CartItem, Order

admin.site.register(Order)
admin.site.register(CartItem)
