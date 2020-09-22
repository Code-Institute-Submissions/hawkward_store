from django.urls import path
from . import views

urlpatterns = [
    path('', views.check_for_free_items, name='check_for_free_items'),
    path('payment_processing', views.payment_processing, name='payment_processing'),
]
