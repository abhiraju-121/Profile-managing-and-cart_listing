from django.contrib import admin
from . models import Product,OrderItem,Order
# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=['name','price']
    search_fields=['name']

admin.site.register(OrderItem)
admin.site.register(Order)