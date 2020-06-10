from django.db import models

class MealType(models.Model):
  SIZE_VARIANTS = (
    ('single', 'single'),
    ('double', 'double')
  )

  name = models.CharField(max_length=50, blank=False, default='type name')
  size_variant = models.CharField(max_length=6, blank=False, choices=SIZE_VARIANTS, default='single')
  is_available = models.BooleanField(default=False)
  image = models.ImageField(default='default_item.png', blank=True, upload_to='media/' )

  class Meta:
    constraints = [
      models.UniqueConstraint(fields=['name'], name='constraint - unique meal type')
    ]


  def __str__(self):
    return f"{self.name}"

class MenuItem(models.Model):
  name = models.CharField(max_length=50, blank=False, default='item name')
  meal_type = models.ForeignKey('MealType', blank=False, related_name='mealType', on_delete=models.CASCADE)
  is_sub = models.BooleanField(default=False) # enables extra cheese option in cart items
  is_available = models.BooleanField(default=False) # to disable from menu, yet not delete from DB
  image = models.ImageField(default='default_item.png', blank=True, upload_to='media/' )

  price_single = models.DecimalField(
    max_digits=5, 
    decimal_places=2,
    default=0.00
  )
  price_small = models.DecimalField(
    max_digits=5, 
    decimal_places=2,
    default=0.00
  )
  price_large = models.DecimalField(
    max_digits=5, 
    decimal_places=2,
    default=0.00
  )

  class Meta:
    constraints = [
      models.UniqueConstraint(fields=['name', 'meal_type'], name='constraint - unique menu item')
    ]


  def __str__(self):
    return f"{self.meal_type}: {self.name}"
  
class Topping(models.Model):
  name = models.CharField(
    max_length=25,
    blank=False,
    default=None,
  )
  is_available = models.BooleanField(default=False) # to disable from menu, yet not delete from DB

  class Meta:
    constraints = [
      models.UniqueConstraint(fields=['name'], name='constraint - unique topping')
    ]


  def __str__(self):
    return f'{self.name}'

class Price(models.Model):
  extra_cheese = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

  neapolitan_small_0_toppings = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
  neapolitan_small_1_toppings = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
  neapolitan_small_2_toppings = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
  neapolitan_small_3_toppings = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
  neapolitan_small_4_toppings = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

  neapolitan_large_0_toppings = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
  neapolitan_large_1_toppings = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
  neapolitan_large_2_toppings = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
  neapolitan_large_3_toppings = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
  neapolitan_large_4_toppings = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

  sicilian_small_0_toppings = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
  sicilian_small_1_toppings = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
  sicilian_small_2_toppings = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
  sicilian_small_3_toppings = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
  sicilian_small_4_toppings = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

  sicilian_large_0_toppings = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
  sicilian_large_1_toppings = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
  sicilian_large_2_toppings = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
  sicilian_large_3_toppings = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
  sicilian_large_4_toppings = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

  def __str__(self):
    return "GLOBAL PIZZA PRICES - EDIT ONLY!!! Don't ever delete this. Don't add new isntances / Prices."


# class CartItem is in the Orders app