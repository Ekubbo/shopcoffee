from django.contrib import admin
from .models import Product, Order, OrderItem
from django.contrib import auth
from django.utils.safestring import mark_safe


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'cost', 'image_tag', )
    prepopulated_fields = {'slug': ('name',), }

    def cost(self, object):
        return "${}.00".format(object.price)

    def image_tag(self, object):
        return mark_safe('<img src="{url}" height="35">'.format(url=object.photo.url))

    image_tag.short_description = 'Image'


class OrderItemInLine(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('subtotal', 'price')
    extra = 0
    can_delete = True

    fieldsets = [
        [None, {
            'fields': ('product', 'price', 'quantity', 'subtotal')
        }],
    ]

    def price(self, object):
        return "${}.00".format(object.product.price)

    def subtotal(self, object):
        cost = object.cost()
        return "${}.00".format(cost)

    def get_formset(self, request, obj=None, **kwargs):
        formset = super(OrderItemInLine, self).get_formset(request, obj, **kwargs)
        form = formset.form
        widget = form.base_fields['product'].widget
        widget.can_add_related = False
        widget.can_change_related = False
        widget.can_delete_related = False
        return formset


class OrderAdmin(admin.ModelAdmin):
    list_filter = ('date_created', )
    list_display = ('first_name', 'phone_client', 'status', 'date_created', 'total_cost')
    readonly_fields = ('total_cost', )
    inlines = [OrderItemInLine]

    fieldsets = [
        ['Contact Information', {
            'fields': [('first_name', 'last_name'), ('phone_client', 'adress_client'),]
        }],
        [None, {
            'fields': ('comment', 'status')
        }],
        [None, {
            'fields': ('total_cost', ),
        }]
    ]

    def total_cost(self, obj):
        result = sum(item.cost() for item in OrderItem.objects.filter(order=obj))
        return "${}.00".format(result)


admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.unregister(auth.models.User)
admin.site.unregister(auth.models.Group)
admin.site.site_header = "SHOP COFFEE ADMIN"
