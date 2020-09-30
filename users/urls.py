from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.users, name='users'),
    path('update_or_create_user/', views.update_or_create_user, name='update_or_create_user'),
    
]
