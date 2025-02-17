from django.contrib import admin

from .models import Order

# Register your models here.


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'status')
    fields = ('id', ('first_name', 'last_name'),
              ('email', 'address'),
              'basket_history', 'status', 'initiator')
    readonly_fields = ('id', 'created')
