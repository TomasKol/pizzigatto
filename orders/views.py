from django.shortcuts import render
from .models import CartItem, Order
from menu.models import *
from django.contrib.auth.models import User
from .helpers import *
from menu.views import mealTypesList

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required


@login_required 
def addtocart(request):
  extraCheese = True if request.POST.get('cheese') else False

  # if such item already is in user's cart, do not add it
  if CartItem.objects.filter(
    menu_item=MenuItem.objects.get(pk=request.POST.get('id')),
    size=request.POST.get('size'),
    user=request.user,
    extra_cheese=extraCheese,
    confirmed=False
  ):
    return JsonResponse({'error': 'such item is already in cart; not adding'})
  
  else:
    # PRICE must be loaded from DB, so the user cannot cheat
    menuItem = MenuItem.objects.get(pk=request.POST.get('id'))
    price = 0.00
    if request.POST.get('size') == 'single':
      price = menuItem.price_single
    elif request.POST.get('size') == 'small':
      price = menuItem.price_small
    elif request.POST.get('size') == 'large':
      price = menuItem.price_large
    else:
      return HttpResponse('unknown size variant', request.POST.get('size'))

    # increase price and change name in case of extra cheese
    name = request.POST.get('name')
    if extraCheese:
      priceObject = Price.objects.get()
      price += priceObject.extra_cheese
      name += ' with extra cheese'

    newCartItem = CartItem(
      name = name,
      menu_item = menuItem,
      amount = 1,
      price_unit = price,
      price_total = price,
      size = request.POST.get('size'),
      extra_cheese = extraCheese,
      user = request.user,
    )
    newCartItem.save()

  return JsonResponse({'message': 'cart item added'})

@login_required
def add_pizza_to_cart(request):

  assert request.method == 'POST'

  toppings = request.POST.getlist('toppings')
  number_of_toppings = len(toppings)
  if number_of_toppings > 4:
    return JsonResponse({'error': 'too many toppings'})
  if not (request.POST.get('form') or request.POST.get('size')):
    return JsonResponse({'error': 'form and size are required'})


  # query for correct pizza price
  price_key = f"{request.POST.get('form')}_{request.POST.get('size')}_{number_of_toppings}_toppings"
  price = getattr(Price.objects.get(), price_key)

  # determine the pizza name (for description)
  name = ' Cheese'
  for i, top in enumerate(toppings):
    if i == len(toppings) - 1:
      name += f' and {getattr(Topping.objects.get(pk=top), "name")}' 
    else:
      name += f', {getattr(Topping.objects.get(pk=top), "name")}' 

  # check if such pizza is already in cart
  if CartItem.objects.filter(
      name=name,
      pizza_form=request.POST.get('form'),
      size=request.POST.get('size'),
      user=request.user,
      confirmed=False
    ).exists():
    return JsonResponse({'error': 'Such pizza is already in'})

  # create CartItem
  CartItem.objects.create(
    name=name,
    amount=1,
    pizza_form=request.POST.get('form'),
    size=request.POST.get('size'),
    price_unit=price,
    price_total=price,
    user=request.user,
  )

  full_name = f"{request.POST.get('size')} {request.POST.get('form').title()} pizza with {name}"
  return JsonResponse({'message': full_name})

@login_required 
def viewcart(request):
  items = CartItem.objects.filter(user=request.user, confirmed=False)
  totalPrice = cartTotal(items)
  context = {'cart': items, 'totalPrice': totalPrice}
  return render(request, 'orders/view_cart.html', context)

@login_required 
def delete_cart_item(request):
  deleteThis = CartItem.objects.get(
    id=request.POST.get('id'), 
    user=request.user
  )

  deleteThis.delete()

  # return the id back, so the FE can remove its corresponding html elements after success
  return JsonResponse({'deletedCartItemId': request.POST.get('id')})

@login_required 
def change_amount(request):

  item = CartItem.objects.get(
    id=request.POST.get('id'), 
    user=request.user
  )

  # do not allow going under amount 1
  if item.amount == 1 and request.POST.get('direction') == '-1':
    pass
  else:
    item.amount += int(request.POST.get('direction')) # +1 or -1
    item.price_total = item.price_unit * item.amount
    item.save()

  context = {
    'amount': item.amount, 
    'priceTotal': item.price_total,
  }

  return JsonResponse(context)

@login_required 
def place_order(request):
  items = CartItem.objects.filter(user=request.user, confirmed=False)
  totalPrice = cartTotal(items)
  context = {'items': items, 'totalPrice': totalPrice}
  return render(request, 'orders/confirm_order.html', context)

@login_required 
def confirm_order(request):
  # create the order from user's cart items not yet placed in a confirmed order
  cartItems = CartItem.objects.filter(user=request.user, confirmed=False)
  order = Order(user=request.user)
  order.save()

  # set items as confirmed in an order and add them to the order
  for item in cartItems:
    item.confirmed = True
    item.save()
    order.items.add(item)
  order.save()

  return redirect('orders:view_my_orders')

@login_required 
def view_my_orders(request):
  orders = Order.objects.filter(user=request.user).order_by('-id')
  context = {'orders': orders}
  return render(request, 'orders/view_my_orders.html', context)

@staff_member_required 
def view_all_orders(request):
  orders = Order.objects.order_by('-id')
  accepted = []
  pending = []
  for order in orders:
    if order.accepted == True:
      accepted.append(order)
    else:
      pending.append(order)

  context = {
    'orders': orders,
  }
  return render(request, 'orders/view_all_orders.html', context) 

@staff_member_required 
def accept_order(request):
  order = Order.objects.get(pk=request.POST.get('id'))
  order.accepted = True
  order.save()

  return HttpResponse('order accepted')

