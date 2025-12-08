from rest_framework.routers import DefaultRouter

from django.urls import include, path

from .views import OfferViewSet

router = DefaultRouter()
router.register(r'offers', OfferViewSet, basename='offer')

urlpatterns = [
    path('', include(router.urls)),
]
