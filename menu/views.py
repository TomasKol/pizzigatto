import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from .models import MealType, MenuItem, Topping, Price
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .forms import PriceForm, MealTypeForm, MenuItemForm, ToppingForm
from django.forms.models import modelformset_factory
from django.db import IntegrityError


def mealTypesList(): 
  # Helper function to retrieve names of all the existant meal types as a list
  mealTypes = MealType.objects.all()
  res = []
  for type in mealTypes:
    res.append(type.name)
  return res

@login_required
def menu(request): 
  mealTypes = MealType.objects.filter(is_available=True)
  menuItems = {}
  for type in mealTypes:
    currentType = MealType.objects.get(pk=type.id)
    menuItems[type] = MenuItem.objects.filter(meal_type=currentType, is_available=True)

  context = {
    'items': menuItems,
    'mealTypes': mealTypes,
    'prices': Price.objects.get(),
    'pizza': {
      'forms': ['napolitana', 'siciliana'],
      'sizes': ['small', 'large'],
      'toppings': Topping.objects.filter(is_available=True),
      'range': [1, 2, 3, 'Special'],
    }
  }

  return render(request, 'menu/menu.html', context=context)

@staff_member_required
def menu_manager(request):
  return manage_meal_types(request)

@staff_member_required 
def edit_global_prices(request):
  priceInstance = Price.objects.get()

  if request.method == 'GET':
    form = PriceForm(instance=priceInstance)
    context = {'form': form}
    return render(request, 'menu/form_price.html', context)

  else:
    # use the new data from user and apply them to the priceInstance
    # (without the instance parameter it will create a new instance)
    assert request.method == 'POST'
    form = PriceForm(request.POST, instance=priceInstance)
    if form.is_valid():
      form.save()

    context = {'form': form}
    return render(request, 'menu/form_price.html', context)

@staff_member_required 
def manage_menu_items(request): # to render the menu manager navbar
  meal_types = MealType.objects.all()
  context = {
    'types': meal_types
  }
  return render(request, 'menu/manage_menu_items.html', context)

# MEAL TYPES
@staff_member_required
def manage_meal_types(request):
  MealTypeFormSet = modelformset_factory(MealType, form=MealTypeForm, extra=0)
  types = MealType.objects.all().order_by('-id')
  formset = MealTypeFormSet(queryset=types)
  context = {
    'formset': formset,
    'add_meal_type': MealTypeForm(),
    'types': types,
  }
  return render(request, 'menu/manage_meal_types.html', context)
  
@staff_member_required 
def add_meal_type(request):
  assert request.method == 'POST'
  form = MealTypeForm(request.POST)
  if form.is_valid():
    form.save()
    return manage_meal_types(request)
  return meal_type_integrity_error(request, err='add')

@staff_member_required 
def edit_meal_types(request):
  assert request.method == 'POST'
  MealTypeFormSet = modelformset_factory(MealType, form=MealTypeForm, extra=0)
  formset = MealTypeFormSet(request.POST)

  if formset.is_valid():
    formset.save()
    return manage_meal_types(request)
  return meal_type_integrity_error(request, err='edit')

def meal_type_integrity_error(request, err):
  if err == 'add':
    integrity_error_add = 'Every meal type must have a unique name. Please avoid duplicates.'
    integrity_error_edit = ''
  else:
    integrity_error_add = ''
    integrity_error_edit = 'Every meal type must have a unique name. Please avoid duplicates. Your changes were not saved.'
  
  MealTypeFormSet = modelformset_factory(MealType, form=MealTypeForm, extra=0)
  types = MealType.objects.all().order_by('-id')
  formset = MealTypeFormSet(queryset=types)
  context = {
    'formset': formset,
    'add_meal_type': MealTypeForm(),
    'types': types,
    'integrity_error_add': integrity_error_add,
    'integrity_error_edit': integrity_error_edit,
  }
  return render(request, 'menu/manage_meal_types.html', context)

@staff_member_required 
def delete_meal_type(request):
  assert request.method == 'POST'
  mealType = MealType.objects.get(pk=request.POST.get('id'))
  if mealType:
    mealType.delete()
    return JsonResponse({'success': 'meal type deleted'})
  return JsonResponse({'error': 'meal type not deleted'})

# MENU ITEMS
@staff_member_required 
def get_editable_menu_items(request, type_id, err):

  meal_type = MealType.objects.get(pk=type_id) 
  items = MenuItem.objects.filter(meal_type=meal_type).order_by('-id')

  MenuItemFormSet = modelformset_factory(MenuItem, form=MenuItemForm, extra=0)
  formset = MenuItemFormSet(queryset=items)

  integrity_error = ''
  if bool(err):
    integrity_error = 'Every menu item of the same meal type must have unique name. Please avoid duplicates.'

  context = {
    'add_form': MenuItemForm(),
    'formset': formset,
    'types': MealType.objects.all().order_by('-id'),
    'meal_type': meal_type,
    'integrity_error': integrity_error,
  }

  return render(request, 'menu/menu_item_forms.html', context)

@staff_member_required
def add_menu_item(request):
  assert request.method == 'POST'
  form = MenuItemForm(request.POST, request.FILES or None)

  if form.is_valid():
    try:
      type = MealType.objects.get(pk=request.POST.get('type_id'))
      new_item = form.save(commit=False)
      # meal_type needs an instance of the type; not only the integer that comes from FE
      new_item.meal_type = type 
      if type.name == 'sub':
        new_item.is_sub = True
      new_item.save()
      return get_editable_menu_items(request, request.POST.get('type_id'), False)

    except IntegrityError:
      type = MealType.objects.get(pk=request.POST.get('type_id'))
      return get_editable_menu_items(request, type.id, err=True)

  return HttpResponse('form not valid')

@staff_member_required 
def edit_menu_item(request):
  assert request.method == 'POST'

  MenuItemFormSet = modelformset_factory(MenuItem, form=MenuItemForm, extra=0)
  formset = MenuItemFormSet(request.POST, request.FILES or None)

  if formset.is_valid():
    try:
      formset.save()
    except IntegrityError:
      return get_editable_menu_items(request, type_id=request.POST.get('type_id'), err=True)

  return get_editable_menu_items(request, type_id=request.POST.get('type_id'), err=False)
  
@staff_member_required 
def delete_menu_item(request):
  assert request.method == 'POST'
  item = MenuItem.objects.get(pk=request.POST.get('id'))
  if item:
    item.delete()
    return JsonResponse({'success': 'item removed'})

  return manage_menu_items(request)

# TOPPINGS
@staff_member_required
def get_editable_toppings(request, err):
  toppings = Topping.objects.all().order_by('-id')
  ToppingFormSet = modelformset_factory(Topping, form=ToppingForm, extra=0)
  formset = ToppingFormSet(queryset=toppings)
  integrity_error = ''

  if bool(err):
    integrity_error = 'Every topping must have a unique name. Please avoid duplicates.'

  context = {
    'add_form': ToppingForm(),
    'formset': formset,
    'types': MealType.objects.all().order_by('-id'),
    'integrity_error': integrity_error,
  }

  return render(request, 'menu/menu_item_toppings.html', context)

@staff_member_required
def add_topping(request):
  assert request.method == 'POST'
  form = ToppingForm(request.POST)
  if form.is_valid():
    form.save()
    return get_editable_toppings(request, err=False)
  return get_editable_toppings(request, err=True)

@staff_member_required
def edit_topping(request):
  assert request.method == 'POST'

  ToppingFormSet = modelformset_factory(Topping, form=ToppingForm, extra=0)
  formset = ToppingFormSet(request.POST)

  if formset.is_valid():
    formset.save()
    return get_editable_toppings(request, err=False)
  return get_editable_toppings(request, err=True)

@staff_member_required
def delete_topping(request):
  assert request.method == 'POST'
  topping = Topping.objects.get(pk=request.POST.get('id'))
  if topping:
    topping.delete()
    return JsonResponse({'success': 'topping deleted'})
  return  get_editable_toppings(request)
