from .serializers import CartItemSerializers
from .models import Product, OrderItem
from rest_framework import serializers


class CartItem():
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity


class Cart():

    max_quantity = 20

    def __init__(self, session):
        self.session = session
        self._items = session["basket"] if "basket" in session else {}

    def clear(self):
        self._items = {}
        self.update_session()

    def get_items(self):
        products = Product.objects.filter(slug__in=self._items.keys())
        return [CartItem(i, self._items[i.slug]) for i in products]

    def data(self):
        return CartItemSerializers(self.get_items(), many=True).data

    def update_session(self):
        self.session["basket"] = self._items

    def add(self, slug, quantity):
        if Product.objects.filter(slug=slug).count() == 0:
            raise serializers.ValidationError("Product does not exist.")

        if slug in self._items:
            self._items[slug] += quantity
        else:
            self._items[slug] = quantity

        self._items[slug] = max(self._items[slug], 1)
        self._items[slug] = min(self._items[slug], self.max_quantity)
        self.update_session()

    def delete(self, slug):
        if slug in self._items:
            self._items.pop(slug)
            self.update_session()
        else:
            raise serializers.ValidationError("Product not in cart.")

    def create_order(self, order):
        for item in self.get_items():
            OrderItem.objects.create(product=item.product, order=order,
                                     quantity=item.quantity)
        self.clear()
