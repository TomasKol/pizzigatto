from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

app_name = 'orders'

urlpatterns = [
    # customer
    path('addtocart/', views.addtocart, name='addtocart'),
    path('add_pizza_to_cart/', views.add_pizza_to_cart, name='add_pizza_to_cart'),
    path('viewcart/', views.viewcart, name='viewcart'),
    path('delete_cart_item/', views.delete_cart_item, name='delete_cart_item'),
    path('change_amount/', views.change_amount, name='change_amount'),
    path('place_order/', views.place_order, name='place_order'),
    path('confirm_order/', views.confirm_order, name='confirm_order'),
    path('view_my_orders/', views.view_my_orders, name='view_my_orders'),

    # staff
    path('view_all_orders/', views.view_all_orders, name='view_all_orders'),
    path('accept_order/', views.accept_order, name='accept_order'),


]

urlpatterns += staticfiles_urlpatterns()