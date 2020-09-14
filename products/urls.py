from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.products, name='products'),
    path('add_product/', views.add_product, name='add_product'),
    path('add_category/', views.add_category, name='add_category'),
]
