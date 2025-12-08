from rest_framework import viewsets, filters

from django.db.models import Min
from django_filters.rest_framework import DjangoFilterBackend


from offer_app.models import Offer
from .serializers import OfferListSerializer
from .filters import OfferFilter


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
