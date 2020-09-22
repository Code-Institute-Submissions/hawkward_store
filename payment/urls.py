from django.urls import path
from . import views

urlpatterns = [
    path('', views.payment_success, name='payment_success'),
]
