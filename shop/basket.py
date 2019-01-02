from .serializers import ProductSerializers
from .models import Product


class Basket():

    def __init__(self, request):
        self.request = request

        if "basket" not in request.session:
            request.session["basket"] = {}

        self.basket = request.session["basket"]

    def addProduct(self, slug, quantity):
        if slug in self.basket:
            self.basket[slug] += quantity
        else:
            self.basket[slug] = quantity
        self.request.session["basket"] = self.basket

    def setProduct(self, slug, quantity):
        self.basket[slug] = quantity

        self.request.session["basket"] = self.basket

    def deleteProduct(self, slug):
        if slug in self.basket:
            self.basket.pop(slug)
        self.request.session["basket"] = self.basket

    def data(self):
        products = Product.objects.filter(slug__in=self.basket.keys())
        serializer = ProductSerializers(products, many=True)
        data_products = serializer.data
        for product in data_products:
            product["quality"] = self.basket[product["slug"]]

        return data_products
