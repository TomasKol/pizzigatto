from django import forms
from .models import Price, MealType, MenuItem, Topping
# from .views import mealTypesList

class MealTypeForm(forms.ModelForm):
    CHOICES = [
        ('single', 'single size'),
        ('double', 'double size')
    ]
    size_variant = forms.ChoiceField(
        choices=CHOICES,
        label='',
        widget=forms.RadioSelect(
            attrs={
                'class': 'li-without-marker'
            }
        )
    )
    name = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'new type',
                'required': 'true',
            }
        )
    )
    is_available = forms.BooleanField(
        label='is available',
        required=False
    )

    image = forms.ImageField(
        initial='default_item.png',
        required=False,
        widget=forms.FileInput,
    )

    class Meta:
        model = MealType
        fields = ['name', 'size_variant', 'is_available', 'image']

class MenuItemForm(forms.ModelForm):
    name = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'new item',
                'required': 'true'
            }
        )
    )
    price_single = forms.DecimalField(
        required=False,
        initial=0.00,
        widget=forms.NumberInput(
            attrs={
                'step': 0.01,
                'min': 0.00,
                'max': 999.99
            }
        )
    )
    price_small = forms.DecimalField(
        required=False,
        initial=0.00,
        widget=forms.NumberInput(
            attrs={
                'step': 0.01,
                'min': 0.00,
                'max': 999.99
            }
        )
    )
    price_large = forms.DecimalField(
        required=False,
        initial=0.00,
        widget=forms.NumberInput(
            attrs={
                'step': 0.01,
                'min': 0.00,
                'max': 999.99
            }
        )
    )
    is_available = forms.BooleanField(
        label='is available',
        required=False
    )
    image = forms.ImageField(
        initial='default_item.png',
        required=False,
        widget=forms.FileInput,
    )

    class Meta:
        model = MenuItem
        fields = ['name', 'price_single', 'price_small', 'price_large', 'is_available', 'image']

class ToppingForm(forms.ModelForm):
    name = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'new topping',
                'required': 'true'
            }
        )
    )
    
    is_available = forms.BooleanField(
        label='is available',
        required=False
    )

    class Meta:
        model = Topping
        fields = ['name', 'is_available']

class PriceForm(forms.ModelForm):
    class Meta:
        model = Price
        fields = ['extra_cheese', 'neapolitan_small_0_toppings', 'neapolitan_small_1_toppings',
                  'neapolitan_small_2_toppings', 'neapolitan_small_3_toppings', 'neapolitan_small_4_toppings', 'neapolitan_large_0_toppings', 'neapolitan_large_1_toppings', 'neapolitan_large_2_toppings',
                  'neapolitan_large_3_toppings', 'neapolitan_large_4_toppings', 'sicilian_small_0_toppings', 'sicilian_small_1_toppings', 'sicilian_small_2_toppings',
                  'sicilian_small_3_toppings', 'sicilian_small_4_toppings', 'sicilian_large_0_toppings', 'sicilian_large_1_toppings', 'sicilian_large_2_toppings',
                  'sicilian_large_3_toppings', 'sicilian_large_4_toppings', ]

    def __init__(self, *args, **kwargs):
        super(PriceForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control price-input'
