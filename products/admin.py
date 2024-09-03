from django.contrib import admin

from .models import Basket, Product, ProductCategory

# Register your models here.


# admin.site.register(ProductCategory)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category')
    search_fields = ('name', )
    list_filter = ('name', 'price')
    fields = ('name', 'description', ('price', 'quantity'), 'stripe_product_price_id', 'image', 'category')
    ordering = ('-price',)


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('product', 'quantity')
    extra = 0


class ProductInCategoryAdmin(admin.TabularInline):
    model = Product
    fields = ('name', 'price', 'quantity')
    extra = 0


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)

    inlines = (ProductInCategoryAdmin, )

