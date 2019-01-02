from .models import Product
from rest_framework import serializers


class ProductSerializers(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('name', 'slug', 'description', 'price', 'photo')
