from rest_framework.routers import DefaultRouter

from django.urls import path, include

from .views import CompletedOrderCountView, OrderViewSet, BusinessOrderView

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
    path('order-count/<int:business_user_id>/',
         BusinessOrderView.as_view(), name='order-count'),
    path('completed-order-count/<int:business_user_id>/',
         CompletedOrderCountView.as_view(), name='completed-order-count'),
]
