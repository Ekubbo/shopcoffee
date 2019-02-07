from .serializers import ProductSerializers, OrderItemSerializers
from .models import Product


class Basket():

    def __init__(self, request):
        self.request = request

        if "basket" not in request.session:
            request.session["basket"] = {}

        self.basket = request.session["basket"]

    def clear(self):
        self.basket = {}
        self.save()

    def save(self):
        self.request.session["basket"] = self.basket

    def addProduct(self, slug, quantity):
        if slug in self.basket:
            self.basket[slug] += quantity
        else:
            self.basket[slug] = quantity

        if self.basket[slug] <= 0:
            self.basket[slug] = 1

        self.save()

    def setProduct(self, slug, quantity):
        if slug in self.basket:
            self.basket[slug] = quantity

            if self.basket[slug] <= 0:
                self.basket[slug] = 1

            self.save()

    def deleteProduct(self, slug):
        if slug in self.basket:
            self.basket.pop(slug)
        self.save()

    def data(self):
        result = []

        for key in self.basket.keys():
            product = ProductSerializers(Product.objects.get(slug=key)).data
            quantity = self.basket[key]
            result.append({'product': product, 'quantity': quantity})

        return result

    def create_order(self, order):
        order_items = []
        for key in self.basket.keys():
            product = Product.objects.get(slug=key)
            quantity = self.basket[key]
            order_items.append({'product': product.id, 'quantity': quantity, 'order': order.id})

        serializers = OrderItemSerializers(data=order_items, many=True)

        if serializers.is_valid():
            serializers.save()
