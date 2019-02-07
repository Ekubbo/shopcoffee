from django.contrib import admin
from .models import Product, Order, OrderItem
from django.utils.safestring import mark_safe


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',), }


class OrderItemInLine(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('cost',)
    extra = 0

    def cost(self, object):
        return str(object.cost())


class OrderAdmin(admin.ModelAdmin):
    list_filter = ('date_created', )
    list_display = ('status', 'date_created', )
    readonly_fields = ('total_cost', )
    inlines = [ OrderItemInLine ]

    def total_cost(self, obj):
        result = 0
        for item in OrderItem.objects.filter(order=obj):
            result += item.cost()
        return result


admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
