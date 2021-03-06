import uuid

from django.db import models
from products.models import ProductsStore
from django.contrib.auth.models import User


class Order(models.Model):
    order_number = models.CharField(max_length=32, null=True, editable=False)
    user_profile = models.ForeignKey(User, on_delete=models.SET_NULL,
                                     null=True, blank=True)
    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    country = models.CharField(max_length=50, null=False, blank=False)
    street_address = models.CharField(max_length=50, null=False, blank=False)
    city = models.CharField(max_length=50, null=False, blank=False)
    postcode = models.CharField(max_length=50, null=False, blank=False)
    phone_number = models.CharField(max_length=50, null=False, blank=False)
    total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0)
    all_products = models.TextField(null=False, blank=False, default='')
    free_products = models.TextField(null=True, blank=True, default='')
    stripe_pid = models.CharField(
        max_length=254, null=False, blank=False, default='')

    def _generate_order_number(self):
        """
        Generate a random, unique order number using UUID
        """
        return uuid.uuid4().hex.upper()

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderItems(models.Model):
    order = models.ForeignKey(Order, null=False, blank=False,
                              on_delete=models.CASCADE)
    product = models.ForeignKey(
        ProductsStore, null=False, blank=False, on_delete=models.CASCADE)
    product_size = models.CharField(
        max_length=2, null=True, blank=True)  # XS, S, M, L, XL
    quantity = models.IntegerField(null=False, blank=False, default=0)
    products_total = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, blank=False, editable=False)

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the lineitem total
        and update the order total.
        """
        self.products_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'SKU {self.product.sku} on order {self.order.order_number}'
