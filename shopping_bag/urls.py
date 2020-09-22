from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.shopping_bag, name='shopping_bag'),    
    path('add/int:<product_id>/', views.add_item_to_bag, name='add_item_to_bag'),
    path('del/int:<product_id>/', views.delete_item_from_bag, name='delete_item_from_bag'),
    path('change/int:<product_id>/', views.change_quantity, name='change_quantity'),
]
