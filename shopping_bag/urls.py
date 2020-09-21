from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.shopping_bag, name='shopping_bag'),    
    path('add/int:<product_id>/', views.add_item_to_bag, name='add_item_to_bag'),
]
