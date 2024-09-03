from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BasketModelViewSet, ProductModelViewSet

router = DefaultRouter()
router.register(r'products', ProductModelViewSet)
router.register(r'baskets', BasketModelViewSet)
app_name = 'api'

urlpatterns = [
    path('', include(router.urls))
]
