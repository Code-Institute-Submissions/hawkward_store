from django.contrib import admin
from .models import ProductsStore, Category, Animals

# Register your models here.


class ProductsStoreAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'sku',
        'name',
        'category',
        'price',
        'has_giftcard',
        'description',
        'image_url',
    )

class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'friendly_name',
        'name',
    )

class AnimalsAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'friendly_name',
        'name',
    )

admin.site.register(ProductsStore, ProductsStoreAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Animals, AnimalsAdmin)
