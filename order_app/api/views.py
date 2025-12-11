from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from django.db.models import Q

from offer_app.models import OfferDetail
from order_app.api.permissions import IsCustomerUser
from order_app.models import Order
from .serializers import OrderSerializer, OrderCreateSerializer


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(Q(customer_user=user) | Q(business_user=user)).order_by('-created_at')

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(), IsCustomerUser()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):

        offer_detail_id = serializer.validated_data.pop('offer_detail_id')
        offer_detail = get_object_or_404(OfferDetail, pk=offer_detail_id)

        business_user = offer_detail.offer.user
        customer_user = self.request.user

        serializer.save(
            business_user=business_user,
            customer_user=customer_user,
            title=offer_detail.title,
            revisions=offer_detail.revisions,
            delivery_time_in_days=offer_detail.delivery_time_in_days,
            price=offer_detail.price,
            features=offer_detail.features,
            offer_type=offer_detail.offer_type,
            status='in_progress'
        )
