from django.views.generic.base import TemplateView
from .serializers import ProductSerializers
from .models import Product
from rest_framework import viewsets


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers


class HomePageView(TemplateView):
    template_name = "home.html"
