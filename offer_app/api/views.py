from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated, AllowAny


from django.db.models import Min
from django_filters.rest_framework import DjangoFilterBackend


from offer_app.models import Offer
from .serializers import OfferListSerializer, OfferCreateSerializer
from .filters import OfferFilter
from .permissions import IsBusinessUser


class OfferViewSet(viewsets.ModelViewSet):
    permission_classes = []

    queryset = Offer.objects.annotate(
        min_price=Min('details__price'),
        min_delivery_time=Min('details__delivery_time_in_days')
    ).order_by('-updated_at')

    serializer_class = OfferListSerializer
    filter_backends = [DjangoFilterBackend,
                       filters.OrderingFilter, filters.SearchFilter]
    filterset_class = OfferFilter
    search_fields = ['title', 'description']
    ordering_fields = ['updated_at', 'min_price']

    def get_serializer_class(self):
        if self.action == 'create':
            return OfferCreateSerializer
        return OfferListSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(), IsBusinessUser()]
        return [AllowAny()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
