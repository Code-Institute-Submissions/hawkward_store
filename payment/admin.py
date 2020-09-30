from django.contrib import admin
from .models import Order, OrderItems

# Register your models here.


class OrderItemsAdminInline(admin.TabularInline):
    model = OrderItems
    readonly_fields = ('products_total',)


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderItemsAdminInline,)

    readonly_fields = ('order_number', 'total',
                       'all_products', 'stripe_pid'
                       )

    fields = ('order_number', 'user_profile', 'first_name',
              'last_name', 'email', 'country',
              'street_address', 'city', 'postcode',
              'phone_number', 'total', 'all_products',
              'free_products', 'stripe_pid')

    list_display = ('order_number', 'first_name',
                    'last_name', 'total',)

    ordering = ('-pk',)


admin.site.register(Order, OrderAdmin)
