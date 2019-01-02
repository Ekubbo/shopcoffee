from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from shop.views import ListProducts, HomePageView, ListBasket, AddToBasket
from shop.views import DeleteFromBasket

urlpatterns = [
    path('', HomePageView.as_view()),
    path('admin/', admin.site.urls),
    path('api/products/', ListProducts.as_view({'get': 'list'})),
    path('api/basket/list/', ListBasket.as_view()),
    path('api/basket/add/', AddToBasket.as_view()),
    path('api/basket/delete/', DeleteFromBasket.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
