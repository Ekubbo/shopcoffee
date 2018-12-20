from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from shop.views import ProductViewSet, HomePageView

urlpatterns = [
    path('', HomePageView.as_view()),
    path('admin/', admin.site.urls),
    path('api/products/', ProductViewSet.as_view({'get': 'list'})),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
