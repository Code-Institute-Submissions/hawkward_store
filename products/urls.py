from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.products, name='products'),
    path('product_management/', views.product_management, name='product_management'),
    path('add_product/', views.add_product, name='add_product'),
    path('add_category/', views.add_category, name='add_category'),
    path('add_animal/', views.add_animal, name='add_animal'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('product_information/<int:product_id>/', views.product_information, name='product_information'),
]
