from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from menu.models import MenuItem

class CartItem(models.Model):
  PIZZA_FORM = (
    ('neapolitan', 'neapolitan'),
    ('sicilian', 'sicilian'),
    ('not pizza', 'not pizza')
  )

  SIZE_OPTIONS = (
    ('single', 'single'),
    ('small', 'small'),
    ('large', 'large')
  )

  name = models.CharField(max_length=100)
  menu_item = models.ForeignKey(MenuItem, blank=True, null=True, on_delete=models.CASCADE, related_name='menu_items')
  amount = models.IntegerField(default=1)
  price_unit = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
  price_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
  size = models.CharField(max_length=6, choices=SIZE_OPTIONS) # small, large, single
  pizza_form = models.CharField(max_length=10, choices=PIZZA_FORM, default='not pizza')
  extra_cheese = models.BooleanField(default=False)
  confirmed = models.BooleanField(default=False)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  # all this info is just for the staff/customer to be displayed, no need to
  # make the foreign keys connection - only User and 
  # menu_item_id to retrieve the real price, should the user somehow cheat on the front end
  
  # item_id is to retrieve the price from DB
  # default 0 is for pizza, where this field is irrelevant (pizza prices are loaded from a Price object)
  # when creating instances of CartItems, the price value is loaded from DB; it never comes from FE (only display)

  def __str__(self):
    type = self.menu_item.meal_type if self.menu_item else 'pizza'
    return f'{self.size if self.size != "single" else ""} {type}: {self.name} {self.amount}x'

class Order(models.Model):
  items = models.ManyToManyField('CartItem', blank=False, related_name='ordered_items')
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  accepted = models.BooleanField(default=False) # staff member marks order as Accepted

  def status(self):
    return 'pending' if self.accepted == False else 'accepted'

  def price(self):
    price = 0
    for item in self.items.all():
      price += item.price_total
    return price

  def __str__(self):
    return f"order {self.id} by {self.user}: {len(self.items.all())} items, ${self.price()}, {self.status()}"

