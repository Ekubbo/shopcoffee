from django.views.generic.base import TemplateView
from .serializers import ProductSerializers, OrderSerializers
from .models import Product
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from .basket import Basket
from rest_framework import status, generics


class ListProducts(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers


class HomePageView(TemplateView):
    template_name = "home.html"


class ListBasket(APIView):

    def get(self, request, format=None):
        basket = Basket(request)
        return Response(basket.data())


class CreateOrder(generics.CreateAPIView):
    serializer_class = OrderSerializers

    def create(self, request, format=None):
        data = request.data
        serializer = self.serializer_class(data=data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        order = serializer.create(serializer.validated_data)

        basket = Basket(request)
        basket.create_order(order)
        basket.clear()

        return Response(status=status.HTTP_200_OK)


class AddToBasket(APIView):

    def is_valid(self, request):
        if "slug" not in request.data or "quantity" not in request.data:
            return False

        try:
            Product.objects.get(slug=request.data['slug'])
        except (Product.DoesNotExist):
            return False

        return True

    def put(self, request, format=None):
        if not self.is_valid(request):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        basket = Basket(request)
        basket.setProduct(**request.data)

        return Response(status=status.HTTP_200_OK)

    def post(self, request, format=None):
        if not self.is_valid(request):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        basket = Basket(request)
        basket.addProduct(**request.data)

        return Response(status=status.HTTP_200_OK)


class DeleteFromBasket(APIView):

    def is_valid(self, request):
        if "slug" not in request.data:
            return False

        try:
            Product.objects.get(slug=request.data['slug'])
        except (Product.DoesNotExist):
            return False

        return True

    def post(self, request):
        if not self.is_valid(request):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        basket = Basket(request)
        basket.deleteProduct(**request.data)

        return Response(status=status.HTTP_200_OK)
