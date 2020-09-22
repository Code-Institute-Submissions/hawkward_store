from django.contrib import admin
from .models import Giftcards

# Register your models here.
class GiftcardsAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'product_id',
        'product_name',
        'counter',
    )

    ordering = ('product_id',)

admin.site.register(Giftcards, GiftcardsAdmin)
