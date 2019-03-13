from django.views.generic.base import TemplateView
from .serializers import ProductSerializers, OrderSerializers
from .models import Product
from rest_framework.views import APIView
from rest_framework.response import Response
from .cart import Cart
from rest_framework import status, generics
from .forms import SlugProductForm, AddProductInCartForm


class ListProducts(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers


class HomePageView(TemplateView):
    template_name = "home.html"


class ListCart(APIView):

    def get(self, request, format=None):
        cart = Cart(request.session)
        return Response(cart.data())


class CreateOrder(generics.CreateAPIView):
    serializer_class = OrderSerializers

    def create(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        order = serializer.create(serializer.validated_data)

        cart = Cart(request.session)
        cart.create_order(order)

        return Response(status=status.HTTP_200_OK)


class AddToCart(APIView):

    def post(self, request, format=None):
        form = AddProductInCartForm(data=request.data)
        if not form.is_valid():
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

        cart = Cart(request.session)
        cart.add(**request.data)

        return Response(status=status.HTTP_200_OK)


class DeleteFromCart(APIView):

    def post(self, request):
        form = SlugProductForm(data=request.data)
        if not form.is_valid():
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

        cart = Cart(request.session)
        cart.delete(request.data["slug"])

        return Response(status=status.HTTP_200_OK)
