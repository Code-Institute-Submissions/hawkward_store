from django.contrib import admin
from .models import Giftcards, UserProfile, UserSubscriptions

# Register your models here.


class GiftcardsAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'product_id',
        'product_name',
        'counter',
    )

    ordering = ('product_id',)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'email',
        'country',
        'street_address',
        'city',
        'postcode',
    )


class UserSubscriptionsAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'subscription',
    )


admin.site.register(Giftcards, GiftcardsAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserSubscriptions, UserSubscriptionsAdmin)
