from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings


from . import views

app_name = 'menu'

urlpatterns = [
    path('', views.menu, name='index'),
    path('menu_manager/', views.menu_manager, name='menu_manager'),
    path('edit_global_prices/', views.edit_global_prices, name='edit_global_prices'),
    path('manage_menu_items/', views.manage_menu_items, name='manage_menu_items'),
    path('manage_meal_types/', views.manage_meal_types, name='manage_meal_types'),
    path('add_meal_type/', views.add_meal_type, name='add_meal_type'),
    path('edit_meal_types/', views.edit_meal_types, name='edit_meal_types'),
    path('delete_meal_type/', views.delete_meal_type, name='delete_meal_type'),
    path('get_editable_menu_items/<int:type_id>/<int:err>/', views.get_editable_menu_items, name='get_editable_menu_items'),
    path('add_menu_item/', views.add_menu_item, name='add_menu_item'),
    path('edit_menu_item/', views.edit_menu_item, name='edit_menu_item'),
    path('delete_menu_item/', views.delete_menu_item, name='delete_menu_item'),
    path('get_editable_toppings/<int:err>/', views.get_editable_toppings, name='get_editable_toppings'),
    path('add_topping/', views.add_topping, name='add_topping'),
    path('edit_topping/', views.edit_topping, name='edit_topping'),
    path('delete_topping/', views.delete_topping, name='delete_topping'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
