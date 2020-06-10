from django.contrib import admin
from .models import MealType, MenuItem, Topping, Price

admin.site.register(MealType)
admin.site.register(MenuItem)
admin.site.register(Topping)


class PriceAdmin(admin.ModelAdmin):
  fields = (
    ('extra_cheese'),
    ('napolitana_small_0_toppings', 'napolitana_small_1_toppings', 'napolitana_small_2_toppings', 'napolitana_small_3_toppings', 'napolitana_small_4_toppings',),
    ('napolitana_large_0_toppings', 'napolitana_large_1_toppings', 'napolitana_large_2_toppings', 'napolitana_large_3_toppings', 'napolitana_large_4_toppings',),
    ('siciliana_small_0_toppings', 'siciliana_small_1_toppings', 'siciliana_small_2_toppings', 'siciliana_small_3_toppings', 'siciliana_small_4_toppings',),
    ('siciliana_large_0_toppings', 'siciliana_large_1_toppings', 'siciliana_large_2_toppings', 'siciliana_large_3_toppings', 'siciliana_large_4_toppings',),
  )

admin.site.register(Price, PriceAdmin)
