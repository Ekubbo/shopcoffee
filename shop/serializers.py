from .models import Product, Order, OrderItem
from rest_framework import serializers


class ProductSerializers(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('name', 'slug', 'description', 'price', 'photo', )


class OrderItemSerializers(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ('quantity', 'product', 'order')


class OrderSerializers(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'


class CartItemSerializers(serializers.Serializer):

    product = ProductSerializers(read_only=False, many=False)
    quantity = serializers.IntegerField()
