from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from shop.views import ListProducts, ListCart, HomePageView, AddToCart
from shop.views import DeleteFromCart, CreateOrder

urlpatterns = [
    path('', HomePageView.as_view()),
    path('admin/', admin.site.urls),
    path('api/products/', ListProducts.as_view()),
    path('api/order/', CreateOrder.as_view()),
    path('api/cart/list/', ListCart.as_view()),
    path('api/cart/add/', AddToCart.as_view()),
    path('api/cart/delete/', DeleteFromCart.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
